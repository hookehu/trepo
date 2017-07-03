#!/bin/sh
protoc --proto_path=protocol-src --cpp_out=protocol protocol-src/*.proto
