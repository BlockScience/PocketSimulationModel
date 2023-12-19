# python -m cProfile -o run_1.pstats run_1.py
# gprof2dot --colour-nodes-by-selftime -f pstats run_1.pstats | \
#     dot -Tpng -o run_1.png


python -m cProfile -o run_2.pstats run_2.py
gprof2dot --colour-nodes-by-selftime -f pstats run_2.pstats | \
    dot -Tpng -o run_2.png