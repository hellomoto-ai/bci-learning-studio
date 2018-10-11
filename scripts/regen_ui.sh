#!/usr/bin/env bash

find . -type f -name '*.ui' | while read src; do
    echo "Converting ${src}"
    tgt="${src/.ui/.py}"
    pyuic5 "${src}" -o "${tgt}"
done

find . -type f -name '*.qrc' | while read src; do
    echo "Converting ${src}"
    IFS='.' read -r -a array <<< "${src}"
    n_elems="${#array[@]}"
    filename="${array[${n_elems}-2]}_rc.py"
    tgt="$(dirname "${src}")/${filename}"
    pyrcc5 "${src}" -o "${tgt}"
done
