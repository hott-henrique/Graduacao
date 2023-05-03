for i in $(seq 1 5);
do
	python3 simulate.py \
		--ode-params 0.03 1.0 0.5 0.08 0.02 0.0 \
		--y0 995 5 0 \
		--tf 15

	echo ''
done | python3 plot.py \
			--output-file .local/gillespie_v0.png

for i in $(seq 1 5);
do
	python3 simulate.py \
		--ode-params 0.03 1.0 0.5 0.08 0.02 0.4 \
		--y0 995 5 0 \
		--tf 15

	echo ''
done | python3 plot.py \
			--output-file .local/gillespie_v1.png

