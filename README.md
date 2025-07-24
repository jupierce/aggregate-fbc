# aggregate-fbc
Searches for ART fbc fragments for a given OCP version and aggregates them into a single FBC.

Example invocation:
```
./aggregate.py --major=4 --minor=18 --output-dir tmp --image-name quay.io/jupierce/fbc-aggregate:4.18 --push
Fetching tags from quay.io/openshift-art/stage-fbc-fragments...
Found 15 matching tags: ['ocp__4.18__cluster-nfd-operator', 'ocp__4.18__clusterresourceoverride-operator', 'ocp__4.18__dpu-operator', 'ocp__4.18__helloworld-operator', 'ocp__4.18__ingress-node-firewall-operator', 'ocp__4.18__local-storage-operator', 'ocp__4.18__ose-aws-efs-csi-driver-operator', 'ocp__4.18__ose-gcp-filestore-csi-driver-operator', 'ocp__4.18__ose-metallb-operator', 'ocp__4.18__ose-secrets-store-csi-driver-operator', 'ocp__4.18__ose-smb-csi-driver-operator', 'ocp__4.18__pf-status-relay-operator', 'ocp__4.18__ptp-operator', 'ocp__4.18__sriov-network-operator', 'ocp__4.18__vertical-pod-autoscaler-operator']
Rendering catalog from image ocp__4.18__cluster-nfd-operator...
Rendering catalog from image ocp__4.18__clusterresourceoverride-operator...
Rendering catalog from image ocp__4.18__dpu-operator...
Rendering catalog from image ocp__4.18__helloworld-operator...
Rendering catalog from image ocp__4.18__ingress-node-firewall-operator...
Rendering catalog from image ocp__4.18__local-storage-operator...
Rendering catalog from image ocp__4.18__ose-aws-efs-csi-driver-operator...
Rendering catalog from image ocp__4.18__ose-gcp-filestore-csi-driver-operator...
Rendering catalog from image ocp__4.18__ose-metallb-operator...
Rendering catalog from image ocp__4.18__ose-secrets-store-csi-driver-operator...
Rendering catalog from image ocp__4.18__ose-smb-csi-driver-operator...
Rendering catalog from image ocp__4.18__pf-status-relay-operator...
Rendering catalog from image ocp__4.18__ptp-operator...
Rendering catalog from image ocp__4.18__sriov-network-operator...
Rendering catalog from image ocp__4.18__vertical-pod-autoscaler-operator...
Combining YAMLs into output directory...
Generating Dockerfile...
Building catalog image: quay.io/jupierce/fbc-aggregate:4.18
[1/2] STEP 1/3: FROM registry.redhat.io/openshift4/ose-operator-registry-rhel9:v4.18 AS builder
[1/2] STEP 2/3: ADD tmp /configs
--> Using cache 624993bb663d967a3fa782089ab45924dd9fe5f32efbf44243aa49fc29f8a661
--> 624993bb663
[1/2] STEP 3/3: RUN ["/bin/opm", "serve", "/configs", "--cache-dir=/tmp/cache", "--cache-only"]
--> Using cache c2a0a9409f846c09c530f33968475049dfc273f07b5fbe01427a484876c9c4e0
--> c2a0a9409f8
[2/2] STEP 1/6: FROM registry.redhat.io/openshift4/ose-operator-registry-rhel9:v4.18
[2/2] STEP 2/6: ENTRYPOINT ["/bin/opm"]
--> Using cache 57d20fc8da8d46410dfff3568718dfc042ae9b3ea79a0f0414fa7d98cf5a44a4
--> 57d20fc8da8
[2/2] STEP 3/6: CMD ["serve", "/configs", "--cache-dir=/tmp/cache"]
--> Using cache b5de589e5f098794ed68d505022b965c12df696afaf98db322484dc6abbb4978
--> b5de589e5f0
[2/2] STEP 4/6: COPY --from=builder /configs /configs
--> Using cache ec375b3c4bd9d169d132204a2a13de4f91f3f01f5f916c73a065e6bafd0297e2
--> ec375b3c4bd
[2/2] STEP 5/6: COPY --from=builder /tmp/cache /tmp/cache
--> Using cache 47aff6edd2c1575dcbb197f6366842dfa84e05ae1f61e198e1f847fd77d6e7c3
--> 47aff6edd2c
[2/2] STEP 6/6: LABEL operators.operatorframework.io.index.configs.v1=/configs
--> Using cache a829b8f450e43f0ecd32fe6c0240158bedc4fe7c41d00adfe46e6dc1bbf93e0a
[2/2] COMMIT quay.io/jupierce/fbc-aggregate:4.18
--> a829b8f450e
Successfully tagged quay.io/jupierce/fbc-aggregate:4.18
Successfully tagged quay.io/jupierce/test:4.18-aggregate-fbc
Successfully tagged localhost/aggregate-image:latest
Successfully tagged localhost/aggregate:latest
a829b8f450e43f0ecd32fe6c0240158bedc4fe7c41d00adfe46e6dc1bbf93e0a
Catalog image built successfully.
Pushing image: quay.io/jupierce/fbc-aggregate:4.18
Getting image source signatures
Copying blob 25c75c34b2e2 skipped: already exists  
Copying blob 0be389694498 skipped: already exists  
Copying blob 555d7bb81c3d skipped: already exists  
Copying blob 4e3b98987705 skipped: already exists  
Copying blob 526913aa44a6 skipped: already exists  
Copying blob ddff7028007e skipped: already exists  
Copying config a829b8f450 done  
Writing manifest to image destination
Storing signatures
```
