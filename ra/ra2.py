
import codecs
import json
import time

import collada as co
import numpy as np
import toml
from tqdm import tqdm

from ra import rtrace as rt
from ra.source import (
    # CircleSource, ConicSource,
    IsotropicSource,
    # SingleRaySource
)

from ra.rayinidir import RayInitialDirections
# from ra.receivers import Receivers
from ra.receivers import setup_receivers
# from ra.sources import Sources
from ra.sources import setup_sources
from ra.controlsair import AlgControls
from ra.controlsair import AirProperties
from ra.room import Geometry, GeometryMat
from ra.absorption_database import load_matdata_from_mat
from ra.absorption_database import get_alpha_s
from ra.statistics import StatisticalMat

class Receiver():
    def __init__(self, position=(0, 0, 0)):
        self.position = np.array(position, dtype=np.float32)


class Plane():
    def __init__(self, name, vertices, normal):
        self.name = name
        self.bbox = False  # by default a plane is part of the room geometry
        self.vertices = np.array(vertices, np.float32)
        self.normal = np.float32(normal)


class Rays():
    '''Each source has its own Rays instance'''
    def __init__(self, ri, rd, niters):
        self.nrays = ri.shape[0]
        self.niters = niters
        self.ris = np.zeros((self.nrays, niters, 3), dtype=np.float32)
        self.rds = np.zeros((self.nrays, niters, 3), dtype=np.float32)
        # fill the first iteration rays positions and directions
        self.ris[:, 0] = ri
        self.rds[:, 0] = rd
        # length of ris and rds, after which ris and rds elements should be
        # ignored
        self.length = np.ones((self.nrays,), dtype=np.int32) * niters


class Simulation():
    def __init__(self, cfgfile):
        self.config = self.load_cfg(cfgfile)
        self.sources = self.setup_sources(self.config)
        
        self.receivers = self.setup_receivers(self.config)
        self.room = self.setup_room(self.config)
        self.bbox = self.setup_bounding_box(self.config, scale=100)
        self.n_escaped_rays = 0

        # self.setup_rays() returns a list of 2D matrices, one matrix per
        # source and each matrix with shape (nverts, niters)
        self.rays = self.setup_rays(self.config, self.sources)

    def load_cfg(self, cfgfile):
        with open(cfgfile, 'r') as f:
            config = toml.loads(f.read())
        return config

    def setup_sources(self, config):
        sources = []
        for s in config['sources']:
            # sources.append(CircleSource(
            #     position=s['position'], direction=(0, 1, 0), nverts=10
            # ))
            sources.append(IsotropicSource(position=s['position'], depth=2))
            # sources.append(SingleRaySource(
            #     position=s['position'], direction=(1, 0, 0)
            # ))
            # sources.append(ConicSource(
            #     position=s['position'],
            #     direction=(1, 0, 0),
            #     radius=0.5,
            #     nverts=100
            # ))
        return sources

    def setup_receivers(self, config):
        receivers = []
        for r in config['receivers']:
            receivers.append(Receiver(position=r['position']))
        return receivers

    def setup_room(self, config):
        room = self.load_dae_geometry(daepath=config['geometry']['room'])
        return room

    def setup_bounding_box(self, config, scale=1):
        bbox = self.load_dae_geometry(daepath=config['geometry']['bbox'])
        for plane in bbox:
            plane.vertices *= scale
            plane.bbox = True
        return bbox

    def load_dae_geometry(self, daepath):
        planes = []
        mesh = co.Collada(daepath)
        for obj in mesh.scene.objects('geometry'):
            for triset in obj.primitives():
                if type(triset) != co.triangleset.BoundTriangleSet:
                    print('Warning: non-supported primitive ignored!')
                    continue
                for i, tri in enumerate(triset):
                    plane = Plane(
                        name='{}-{}'.format(obj.original.name, i),
                        vertices=tri.vertices,
                        normal=tri.normals[0] / np.linalg.norm(tri.normals[0])
                    )
                    planes.append(plane)
        return planes

    def setup_rays(self, config, sources):
        # niters = int(np.ceil(np.log(pth/pin) / np.log(1 - alpha)))
        niters = 100
        rays = [Rays(s.ris, s.rds, niters) for s in sources]
        return rays

    def ray_x_planes(self, r0, rd):
        ret_t = np.inf
        ret_plane = None
        ret_ri = np.array([np.inf, np.inf, np.inf], np.float32)

        # test ray against room planes
        for plane in self.room:
            t, ri, hit = rt.ray_x_polygon(r0, rd, plane.vertices, plane.normal)
            if hit and t < ret_t:
                ret_t = t
                ret_plane = plane
                ret_ri = ri
        # if there was no intersection, this ray escaped and we need to test it
        # against the bounding box
        if ret_plane is None:
            self.n_escaped_rays += 1
            ret_t = np.inf
            ret_plane = None
            ret_ri = np.array([np.inf, np.inf, np.inf], np.float32)
            for plane in self.bbox:
                t, ri, hit = rt.ray_x_polygon(
                    r0, rd, plane.vertices, plane.normal
                )
                if hit and t < ret_t:
                    ret_t = t
                    ret_plane = plane
                    ret_ri = ri
        return (ret_plane, ret_ri)

    def start(self):
        # loop through every single ray
        for src_rays in self.rays:
            print(src_rays.nrays)
            progress = tqdm(np.ndindex((src_rays.nrays, src_rays.niters)))
            for (rayid, rayit) in progress:
                if src_rays.length[rayid] != src_rays.niters:
                    continue
                plane, rhit = self.ray_x_planes(
                    r0=src_rays.ris[rayid, rayit],
                    rd=src_rays.rds[rayid, rayit]
                )

                try:
                    src_rays.ris[rayid, rayit+1] = rhit
                except IndexError:
                    # trying to add an element beyond the array size. Using a
                    # try/except block is faster than using an if statement
                    pass
                else:
                    # compute the new direction but first check if this plane
                    # is part of the bounding box
                    if plane.bbox:
                        src_rays.length[rayid] = rayit + 2
                    rd = src_rays.rds[rayid, rayit]
                    n = plane.normal
                    rr = -2*np.dot(rd, n)*n + rd
                    src_rays.rds[rayid, rayit+1] = rr

    def dump(self):
        print('number of escaped rays: {}/{}={}%'.format(
                self.n_escaped_rays,
                self.rays[0].nrays,
                np.around(
                    100 * self.n_escaped_rays / self.rays[0].nrays, decimals=2
                )
        ))
        rays = []
        for r in self.rays:
            rays.append({
                'ris': r.ris.tolist(),
                'length': r.length.tolist()
            })
        sim_json = {'rays': rays}
        json.dump(
            sim_json,
            codecs.open('sim.json', 'w', encoding='utf-8'),
            separators=(',', ':'),
            sort_keys=True,
            # indent=4
        )


def main():

    ##### Test Alg controls ########
    controls = AlgControls('simulation.toml')
    # controls.setup_controls()
    # print(controls.Nrays)
    # print(controls.freq)
    # print(controls.Dt)
    # print(controls.alow_growth)

    ##### Test Alg controls ########
    air = AirProperties('simulation.toml')
    air_m = air.air_absorption(controls.freq)
    # print(air.rho0)
    # print(air.c0)
    # print(air.m)

    ##### Test materials #############
    alpha_list = load_matdata_from_mat('simulation.toml')  
    alpha, s = get_alpha_s('surface_mat_id.toml', alpha_list)
    
    ##### Test Geometry ###########
    geo = GeometryMat('simulation.toml', alpha, s)
    geo.plot_mat_room(normals = 'on')
    # geo = Geometry('simulation.toml')
    #geo.plot_dae_room(normals = 'on')
    # for plane in geo.planes:
    #     print("Plane absorption coefficient: {}.".format(plane.alpha))
    #     print("Plane scaterring coefficient: {}.".format(plane.s))

    #     print("Plane name: {}.".format(plane.name))
    #     print("Plane normal: {}.".format(plane.normal))
    #     print("Plane vertices: {}.".format(plane.vertices))
    #     print("Plane v_x: {}. Plane v_y: {}.".format(plane.vert_x, plane.vert_y))
    #     print("Plane centroid: {}.".format(plane.centroid))
    
    # print("The total area is {} m2.".format(geo.total_area))
    # print("The volume is {} m3.".format(geo.volume))
    
    
    

    ##### Test ray initiation ########
    rays_i_v = RayInitialDirections()
    rays_i_v.isotropic_rays(100)
    # rays_i_v.plot_arrows()
    # rays_i_v.plot_points()
    # print("Rays original directions: {}.".format(rays_i_v.vinit))
    
    ##### Test sources initiation ########
    sources = setup_sources('simulation.toml')
    # for js, s in enumerate(sources):
    #     print("Source {} coord: {}.".format(js, s.coord))
    #     print("Source {} orientation: {}.".format(js, s.orientation))
    #     print("Source {} power dB: {}.".format(js, s.power_dB))
    #     print("Source {} eq dB: {}.".format(js, s.eq_dB))
    #     print("Source {} power (linear): {}.".format(js, s.power_lin))

    
    ##### Test receiver initiation ########
    receivers = setup_receivers('simulation.toml')
    # for jrec, r in enumerate(receivers):
    #     print("Receiver {} coord: {}.".format(jrec, r.coord))
    #     print("Receiver {} coord: {}.".format(jrec, r.orientation))


    ##### Test statistical theory ############
    res_stat = StatisticalMat(geo, controls.freq, air.c0, air_m)
    res_stat.t60_sabine()
    res_stat.t60_eyring()
    res_stat.t60_kutruff(gamma=0.4)
    res_stat.t60_araup()
    res_stat.t60_fitzroy()
    res_stat.t60_milsette()
    
    res_stat.plot_t60()

if __name__ == '__main__':
    main()
