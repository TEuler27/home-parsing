cd \
mkdir home-parsing-temp
move \home-parsing\opzioni.json \home-parsing-temp
rmdir /S /Q \home-parsing
cd \
git clone https://www.github.com/edo1998/home-parsing
move /Y \home-parsing-temp\opzioni.json \home-parsing
rmdir \home-parsing-temp
