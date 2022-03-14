FROM quay.io/pypa/manylinux2014_x86_64:latest AS builder

WORKDIR /home
ARG GRAPHBLAS_VERSION="3.3.3"
ARG BUILD_JOBS=24
RUN curl https://github.com/DrTimothyAldenDavis/GraphBLAS/archive/refs/tags/v$GRAPHBLAS_VERSION.tar.gz -L --output g.tar.gz
RUN tar -xvf g.tar.gz
WORKDIR /home/GraphBLAS-$GRAPHBLAS_VERSION
RUN make JOBS=$BUILD_JOBS && make install

WORKDIR /home
ARG LAGRAPH_VERSION="13June2020"
RUN curl https://github.com/GraphBLAS/LAGraph/archive/$LAGRAPH_VERSION.tar.gz -L --output l.tar.gz
RUN tar -xvf l.tar.gz
WORKDIR /home/LAGraph-$LAGRAPH_VERSION
RUN make JOBS=$BUILD_JOBS && make install

WORKDIR /usr/local/lib64
RUN patchelf "libgraphblas.so.$GRAPHBLAS_VERSION" --set-soname "libgraphblas.so.$GRAPHBLAS_VERSION"
RUN patchelf "libgraphblas.so.$GRAPHBLAS_VERSION" --set-rpath "\$ORIGIN" --force-rpath
RUN patchelf "liblagraph.so.0.1.0" --set-rpath "\$ORIGIN" --force-rpath
RUN patchelf "liblagraph.so.0.1.0" --set-soname "liblagraph.so.0.1.0"
RUN patchelf "liblagraph.so.0.1.0" --replace-needed "libgraphblas.so.3" "libgraphblas.so.$GRAPHBLAS_VERSION"
RUN mkdir -p /lagraph.libs && mv "liblagraph.so.0.1.0" /lagraph.libs && mv "libgraphblas.so.$GRAPHBLAS_VERSION" /lagraph.libs

FROM quay.io/pypa/manylinux2014_x86_64:latest AS bdist_wheel
WORKDIR /home/app
COPY . .
COPY --from=builder /lagraph.libs ./lagraph.libs
RUN /opt/python/cp38-cp38/bin/python setup.py bdist_wheel
