```
seq 10000 | xargs -n 1 -P 10000 -I {} curl -s -o /dev/null http://autoscale-example.default.10.104.27.241.sslip.io 
```