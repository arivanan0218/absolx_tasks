class CelestialBody {
  final String id;
  final String name;
  final String description;
  final String type;
  final String size;
  final String distanceFromEarth;
  final List<String> facts;
  final String imageUrl;

  CelestialBody({
    required this.id,
    required this.name,
    required this.description,
    required this.type,
    required this.size,
    required this.distanceFromEarth,
    required this.facts,
    required this.imageUrl,
  });
}
