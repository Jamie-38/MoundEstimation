# MoundEstimation — Geospatial Mound Density Estimation from Drone Orthophotos (YOLOv8)

This repo contains the **core pipeline code** from my MSc dissertation project, later updated from **Mask R-CNN → YOLOv8 segmentation**.

**Goal:** detect soil mounds created during forestry site preparation from **drone imagery**, convert detections into **georeferenced GIS outputs**, and enable **mound density estimation** in tools like **QGIS**.

> **Portfolio note:** this is a *case study / code snapshot*. The original drone dataset and build environment used during the dissertation are no longer available, so this repo is not provided as a fully reproducible training + evaluation package. The focus here is the **pipeline design and geospatial post-processing**.

---

## What this system does

1. **Orthomosaic / orthophoto creation**  
   Drone images are processed into a single **georeferenced orthophoto** (GeoTIFF).  
   In the original workflow this was produced using **WebODM (Fast Ortho)**.

2. **Tile-based streaming inference**  
   The orthophoto is too large to run inference on as one image, so it is streamed as **512×512 tiles** to keep memory and compute manageable.

3. **YOLOv8 segmentation**  
   Each tile is passed through a YOLOv8 segmentation model trained using transfer learning (COCO weights as a starting point).

4. **Geospatial conversion + GIS export**  
   Mask pixel coordinates are converted into **map coordinates** using the orthophoto’s **affine geotransform**, and detections are exported as **GIS-ready shapefiles**.

5. **Visualisation and analysis**  
   Outputs are intended to be opened in **QGIS** for inspection, mapping, and density calculations.

---

## Results (example)

The images below show:
- the processed orthophoto of a site, and
- a zoomed view with detected mound geometries.

![site_image](https://github.com/Jamie-38/MoundEstimation/assets/85198881/344196bd-e15e-4981-8838-592a609e5744)

![zoom](https://github.com/Jamie-38/MoundEstimation/assets/85198881/d7c9fd15-91b1-4caa-8c96-8d1c5f3aa8ce)

---

## Training approach (high level)

The YOLOv8 model was trained in two phases:

- **Phase 1:** manual labels (~200 images + augmentation), trained for ~100 epochs  
- **Phase 2:** pseudo-labelling to expand the dataset (≈3400 images incl. augmentation), reviewed, then trained for ~100 epochs

Further training and systematic evaluation were planned but became impractical without GPU access and the original dataset.

---

## Repo structure

- `Streamer.py` — streams tiled sections from a georeferenced orthophoto (GeoTIFF) and adjusts geotransforms per tile  
- `Model.py` — wraps YOLOv8 inference  
- `Interface.py` — orchestrates streaming → inference → postprocessing → output, with buffered writes  
- `Interface_utils.py` — mask pixel → geospatial conversion + memory sizing helper  
- `Shapefile.py` — writes detections to ESRI Shapefile using GDAL/OGR  
- `Detection_Result.py` — dataclass representing a single detection (confidence + geospatial coords)

---

## Key engineering / geospatial concepts demonstrated

- **Large raster handling** via tiled streaming rather than loading full orthophotos into memory  
- **Affine geotransform mapping** from pixel space → map space for GIS-aligned outputs  
- **Memory-bounded buffering** of detection results before flushing to disk  
- **Interoperability** with common geospatial tooling (GeoTIFF, EPSG/CRS, Shapefile, QGIS)

---

## Limitations

- This repo does **not** include the original dataset, training environment, or a fully reproducible pipeline.  
- Output quality depends on orthophoto quality (no GCPs available during this work) and the trained model weights.  
- Evaluation tooling (metrics, validation pipeline) exists in the original dissertation work but is not included in this snapshot.

---

## Context

This code is derived from my MSc dissertation work on applying computer vision to forestry site preparation to automate mound detection and support site density estimation using GIS workflows.
