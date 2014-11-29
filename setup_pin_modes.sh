for pin in `cat pins/back* pins/for* pins/waiting pins/ip_address`; do
  gpio mode $pin out
done
for pin in `cat pins/pwm*`; do
  gpio -g mode $pin out
done
