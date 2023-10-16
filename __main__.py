#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import multiprocessing

profile = 'local'
# profile = 'develop'
# profile = 'production'

multiprocessing.freeze_support()
if __name__ == '__main__':
    from ui import main

    main()
