binary:
	bash -c "time nuitka3 uplink"

fullbinary:
	bash -c "time nuitka3 --follow-imports uplink"

standalone:
	bash -c "time nuitka3 --follow-imports --standalone uplink"

clean:
	rm -rf uplink.build/*
	rm -rf uplink.dist/*
	rm -rf uplink.bin

