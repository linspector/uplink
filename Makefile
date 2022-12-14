binary:
	bash -c "time nuitka3 uplink"

fullbinary:
	bash -c "time nuitka3 --follow-imports uplink"

standalone:
	bash -c "time nuitka3 --standalone uplink"

clean:
	rm -rf uplink.build
	rm -rf uplink.dist
	rm -rf uplink.bin
	rm -rf uplink-bin.tar.gz
	rm -rf uplink-bin.7z

run:
	./uplink ./config.json -fsv

runbin:
	./uplink.dist/uplink ./config.json -fsv

targz:
	rm -rf uplink-bin.tar.gz
	tar -czf uplink-bin.tar.gz uplink.dist

tarxz:
	rm -rf uplink-bin.tar.xz
	tar -cJf uplink-bin.tar.xz uplink.dist

7z:
	rm -rf uplink-bin.tar.xz
	7z a uplink-bin.tar.7z uplink.dist

all:
	make clean
	make fullbinary
	make standalone
	make targz
	make 7z

