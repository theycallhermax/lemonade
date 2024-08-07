VERSION := "0.4.0"

build:
	@blueprint-compiler batch-compile \
		src/ui \
		src/ui \
		src/ui/window.blp
	@cargo build --features devel

build-release:
	@blueprint-compiler batch-compile \
		src/ui \
		src/ui \
		src/ui/window.blp
	@cargo build --release

build-flatpak:
	@flatpak-builder \
		--force-clean \
		--install \
		--user \
		--repo=.build/repo \
		.build \
		build-aux/flatpak/ht.sr.git.shrimple.Ouch.json
	@flatpak build-bundle \
		.build/repo \
		ht.sr.git.shrimple.Ouch.flatpak \
		ht.sr.git.shrimple.Ouch \
		--runtime-repo=https://flathub.org/repo/flathub.flatpakrepo

	
run:
	@blueprint-compiler batch-compile \
		src/ui \
		src/ui \
		src/ui/window.blp
	@cargo run --features devel
