#!/usr/bin/env python3

import argparse
import pathlib
import subprocess
import json
import os
import shutil
import tempfile

REPO = "quay.io/openshift-art/stage-fbc-fragments"


def list_tags():
    result = subprocess.run([
        "skopeo", "list-tags", f"docker://{REPO}"
    ], capture_output=True, check=True, text=True)
    return json.loads(result.stdout)["Tags"]


def matches_tag(tag, major, minor):
    return tag.startswith(f"ocp__{major}.{minor}__")


def render_catalog(tag, dest_dir):
    image_ref = f"{REPO}:{tag}"
    output_path = os.path.join(dest_dir, f"{tag}.yaml")
    with open(output_path, "w") as f:
        subprocess.run([
            "opm", "render", image_ref, "-o", "yaml"
        ], check=True, stdout=f)


def main():
    parser = argparse.ArgumentParser(description="Aggregate OLM FBC fragments by version prefix.")
    parser.add_argument("--major", type=int, required=True, help="OCP major version")
    parser.add_argument("--minor", type=int, required=True, help="OCP minor version")
    parser.add_argument("--output-dir", default="aggregated-fbc", help="Output directory for aggregated FBC YAMLs")
    parser.add_argument("--image-name", help="Optional: name of the final built catalog image")
    parser.add_argument("--base-image", help="Base image to use in the catalog (defaults to OCP registry image)")
    parser.add_argument("--builder-image", help="Builder image to use in the catalog (defaults to OCP registry image)")
    parser.add_argument("--push", action="store_true", help="Push the image after building")
    parser.add_argument("--runtime", default="podman", help="Container runtime to use (default: podman)")

    args = parser.parse_args()

    generated_dockerfile_name = f'{args.output_dir}.Dockerfile'
    if args.image_name:
        if pathlib.Path(generated_dockerfile_name).exists():
            print(f'{generated_dockerfile_name} already exists. Delete it before running this command.')
            exit(1)

    major = args.major
    minor = args.minor

    default_image = f"registry.redhat.io/openshift4/ose-operator-registry-rhel9:v{major}.{minor}"
    base_image = args.base_image or default_image
    builder_image = args.builder_image or default_image

    print(f"Fetching tags from {REPO}...")
    tags = list_tags()
    matching_tags = [tag for tag in tags if matches_tag(tag, major, minor)]

    print(f"Found {len(matching_tags)} matching tags: {matching_tags}")
    if not matching_tags:
        print("No matching tags found.")
        return

    os.makedirs(args.output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        for tag in matching_tags:
            print(f"Rendering catalog from image {tag}...")
            render_catalog(tag, temp_dir)

        print("Combining YAMLs into output directory...")
        for filename in os.listdir(temp_dir):
            shutil.copy(os.path.join(temp_dir, filename), os.path.join(args.output_dir, filename))

    print("Generating Dockerfile...")
    subprocess.run([
        "opm", "generate", "dockerfile", args.output_dir,
        "--base-image", base_image,
        "--builder-image", builder_image
    ], check=True)

    if args.image_name:
        print(f"Building catalog image: {args.image_name}")
        subprocess.run([
            args.runtime, "build", "-t", args.image_name, '-f', generated_dockerfile_name
        ], check=True)
        print("Catalog image built successfully.")

        if args.push:
            print(f"Pushing image: {args.image_name}")
            subprocess.run([
                args.runtime, "push", args.image_name
            ], check=True)


if __name__ == "__main__":
    main()
