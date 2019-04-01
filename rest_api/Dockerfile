FROM rust:latest

RUN apt-get update && apt-get install -y unzip libzmq3-dev protobuf-compiler

WORKDIR /project/cert_registry

COPY . .

WORKDIR rest_api
RUN rustup override set nightly-2018-12-05
RUN cargo build

ENV PATH=$PATH:/project/cert_registry/rest_api/target/debug/
