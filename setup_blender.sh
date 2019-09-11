#!/usr/bin/env bash
#
# Installs RA into blender's python installation.
#
# Usage: ./setup_blender.sh -b <BLENDER_DIR> -r <RA_PACKAGE>
#
#   BLENDER_DIR: path to blender's root directory
#
#   RA_PACKAGE: either path to RA project directory (setup.py)
#       or path to RA wheel (ra-*.whl)
#       or git+ssh path (git+ssh://git@github.com/gmagno/ra.git)
#
#
# Note: the Python 3.7.0 headers are downloaded from
# https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz. This version
# should match the one that comes with Blender installation. If a different
# version is needed change var `PYTHON_SOURCE` accordingly.
#

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -b|--blender-dir)
    BLENDER_DIR="$2"
    shift
    shift
    ;;
    -r|--ra-dir)
    RA_PKG="$2"
    shift
    shift
    ;;
    --default)
    DEFAULT=YES
    shift
    ;;
    *)
    POSITIONAL+=("$1")
    shift
    ;;
esac
done
set -- "${POSITIONAL[@]}"

echo "BLENDER DIR  = ${BLENDER_DIR}"
echo "RA PKG  = ${RA_PKG}"

if [ -z "$BLENDER_DIR" ]; then
    echo "ERROR: Unrecognized Blender directory..."
    exit 1
fi

if [ -z "$RA_PKG" ]; then
    echo "ERROR: Unrecognized RA package..."
    exit 1
fi

if [[ -n $1 ]]; then
    echo "ERROR: Unrecognized flags '${POSITIONAL[@]}'!"
    exit 1
fi

export BLENDER_PYTHON=${BLENDER_DIR}/2.80/python/bin/python3.7m
export PYTHON_SOURCE=https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz

wget -qO- ${PYTHON_SOURCE} | \
    tar --strip-components=2 \
        -C ${BLENDER_DIR}/2.80/python/include/python3.7m \
        -zx Python-3.7.0/Include
${BLENDER_PYTHON} -m ensurepip
${BLENDER_PYTHON} -m pip install -U pip
${BLENDER_PYTHON} -m pip install --no-binary=numpy-quaternion ${RA_PKG}
