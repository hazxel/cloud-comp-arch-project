export KOPS_STATE_STORE=gs://cca-eth-2022-group-24-boyan/
export KOPS_FEATURE_FLAGS=AlphaAllowGCE # to unlock the GCE features
export PROJECT=`gcloud config get-value project`
kops create -f part3.yaml
kops create secret --name part3.k8s.local sshpublickey admin -i ~/.ssh/cloud-computing.pub
kops update cluster --name part3.k8s.local --yes --admin