# Waymo Dataset to Lanelet

The purpose of this repository is to convert the Waymo-dataset to Lanelet.

Waymo-dataset: https://github.com/waymo-research/waymo-open-dataset

Lanelet: https://github.com/fzi-forschungszentrum-informatik/liblanelet

Lanelet utilizes OSM(OpenStreeMap) data structure for modelling lanes and their relations. Lanes always contain a left and right polyline while other properties can be assigned to them as well.
Thus, this repo offers a parser which is able to convert multiple lanes into a XML/OSM file. The required input is a list of [left_points, right_points, velocity].

Loading up the waymo-dataset it consists of multiple polylines forming different intersections. Unfortunately, none of these lines represent a total left/right lane but a chunk of it. Therefore, it is hard to determine which polyline follows another polyline.
A workaround is introduced in this repo, although it is working solely for a certain type of road graph.

Since developing a proper method exceeds the workload and might not scale, the work on this repo is stopped.

