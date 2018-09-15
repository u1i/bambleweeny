# perftest: create resources

wrk2 -d30 -R10 -s wrk2_post.lua http://localhost:8080
