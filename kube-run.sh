# Run the deployment
kubectl run b9y --image=u1ih/bambleweeny:latest --env="redis_host=172.17.0.1" --env "redis_port=6379" --port=8080

# Create a Service
kubectl expose deployment b9y --type=NodePort

# Scale up to 5 replicas
kubectl scale deployments/b9y --replicas=5

# Show the endpoint
kubectl get services | grep b9y
