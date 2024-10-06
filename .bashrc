source ./venv/bin/activate
CUR_DIR=$(pwd)
export PATH=$PATH:$CUR_DIR/third_party/riscv64-unknown-elf-gcc-10.1.0-2020.08.2-x86_64-linux-ubuntu14/bin
pip3 install amaranth-yosys
