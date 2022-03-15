#! /usr/bin/env bash

GRAPHBLAS_VERSION="3.3.3"
GRAPHBLAS_MAJOR_VERSION=$(echo "$GRAPHBLAS_VERSION" | cut -d '.' -f 1)
LAGRAPH_VERSION="13June2020"
BUILD_JOBS=8

mkdir -p build && cd build || exit

# Download phase
GRAPHBLAS_ARCHIVE="graphblas-$GRAPHBLAS_VERSION.tar.gz"
[ ! -f "$GRAPHBLAS_ARCHIVE" ] && {
  echo "$GRAPHBLAS_ARCHIVE does not exist. Downloading..."
  curl https://github.com/DrTimothyAldenDavis/GraphBLAS/archive/refs/tags/v$GRAPHBLAS_VERSION.tar.gz -L --output $GRAPHBLAS_ARCHIVE
}

LAGRAPH_ARCHIVE="lagraph-$LAGRAPH_VERSION.tar.gz"
[ ! -f "$LAGRAPH_ARCHIVE" ] && {
  echo "$LAGRAPH_ARCHIVE does not exist. Downloading..."
  curl https://github.com/GraphBLAS/LAGraph/archive/$LAGRAPH_VERSION.tar.gz -L --output $LAGRAPH_ARCHIVE
}

# Extract phase
GRAPHBLAS_DIR="GraphBLAS-$GRAPHBLAS_VERSION"
[ ! -d "$GRAPHBLAS_DIR" ] && {
  echo "$GRAPHBLAS_DIR does not exist. Extracting $GRAPHBLAS_ARCHIVE..."
  tar -xvf "$GRAPHBLAS_ARCHIVE"
}

LAGRAPH_DIR="LAGraph-$LAGRAPH_VERSION"
[ ! -d "$LAGRAPH_DIR" ] && {
  echo "$LAGRAPH_DIR does not exist. Extracting $LAGRAPH_ARCHIVE..."
  tar -xvf "$LAGRAPH_ARCHIVE"
}

# Build phase
( cd "$GRAPHBLAS_DIR" && make JOBS="$BUILD_JOBS" )
# Allow LAGraph to discover GraphBLAS next to itself.
rm -rf "GraphBLAS" && ln -s "$GRAPHBLAS_DIR" "GraphBLAS"
( cd "$LAGRAPH_DIR" && make JOBS="$BUILD_JOBS" )

echo "Building has completed..."

# Patch phase
LIBGRAPHBLAS="libgraphblas.$GRAPHBLAS_VERSION.dylib"
LIBLAGRAPH="liblagraph.0.1.0.dylib"

cd ..
rm -rf lagraph.libs && mkdir -p lagraph.libs
cp "build/$GRAPHBLAS_DIR/build/$LIBGRAPHBLAS" "lagraph.libs"
cp "build/$LAGRAPH_DIR/build/$LIBLAGRAPH" "lagraph.libs"

pushd "lagraph.libs" || exit
install_name_tool "$LIBGRAPHBLAS" -id "@rpath/$LIBGRAPHBLAS"
install_name_tool "$LIBGRAPHBLAS" -add_rpath "@loader_path"
install_name_tool "$LIBLAGRAPH" -id "@rpath/$LIBLAGRAPH"
install_name_tool "$LIBLAGRAPH" -add_rpath "@loader_path"
install_name_tool "$LIBLAGRAPH" -change "@rpath/libgraphblas.$GRAPHBLAS_MAJOR_VERSION.dylib" "@rpath/$LIBGRAPHBLAS"
popd || exit

echo "Patching has completed..."

python3 setup.py bdist_wheel