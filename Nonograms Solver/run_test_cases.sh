dir="nonogramas"
for f in "$dir"/*; do
  python3 resolverNonograma.py "${f##*/}"
done