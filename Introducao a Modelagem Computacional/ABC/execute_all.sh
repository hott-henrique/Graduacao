python3 simulate.py \
	--solver rk4 \
	--ode-params 0.1 0.1 \
	--y0 50 25 0 \
	--tf 10 \
	--dt 0.1 \
	| python3 plot.py \
		--output-file ".local/abc.png"

