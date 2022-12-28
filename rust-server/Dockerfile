FROM rust:1.61

COPY ./ ./
COPY Cargo.toml Cargo.toml

RUN cargo build --release
CMD ["./target/release/rust-server"]
