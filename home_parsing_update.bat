cd \
mkdir home-parsing-temp
move \home-parsing\opzioni.json \home-parsing-temp
rmdir \home-parsing /S /Q
cd \
git clone https://www.github.com/edo1998/home-parsing
move \home-parsing-temp\opzioni.json \home-parsing /Y
rmdir \home-parsing-temp
