for pin in `cat pins/back* pins/for*`; do
  gpio mode $pin out
done
for pin in `cat pins/pwm*`; do
  gpio -g mode $pin out
done
