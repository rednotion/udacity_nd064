## ArgoCD Manifests 

Place the ArgoCD manifests in this directory.

Apply in Vagrant SSH with
```{bash}
kubectl apply -f helm-techtrends-prod.yaml
kubectl apply -f helm-techtrends-staging.yaml
```