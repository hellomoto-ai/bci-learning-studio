#!/usr/bin/env bash

find . -type f -name '*.ui' | while read src; do
    echo "Converting ${src}"
    tgt="${src/.ui/.py}"
    pyuic5 "${src}" -o "${tgt}"
done

# pyrcc5 bci_learning_studio/qt/bci_learning_studio.qt.resource.qrc -o bci_learning_studio/qt/resource_rc.py
