import 'package:flutter/foundation.dart';
import '../models/celestial_body.dart';

class SpaceProvider with ChangeNotifier {
  final List<CelestialBody> _celestialBodies = [
    CelestialBody(
      id: '1',
      name: 'Mars',
      description: 'The Red Planet, fourth planet from the Sun',
      type: 'Planet',
      size: '6,792 km diameter',
      distanceFromEarth: '225 million km',
      facts: [
        'Mars has the largest volcano in the solar system',
        'Mars has two moons: Phobos and Deimos',
        'Mars\' red color comes from iron oxide (rust) on its surface'
      ],
      imageUrl: 'assets/images/mars.jpg',
    ),
    CelestialBody(
      id: '2',
      name: 'Sirius',
      description: 'The brightest star in Earth\'s night sky',
      type: 'Star',
      size: '2.4 million km diameter',
      distanceFromEarth: '8.6 light years',
      facts: [
        'Sirius is actually a binary star system',
        'It\'s also known as the Dog Star',
        'Its surface temperature is about 9,940°C'
      ],
      imageUrl: 'assets/images/sirius.jpeg',
    ),
    CelestialBody(
      id: '3',
      name: 'Andromeda Galaxy',
      description: 'The nearest major galaxy to the Milky Way',
      type: 'Galaxy',
      size: '220,000 light years diameter',
      distanceFromEarth: '2.537 million light years',
      facts: [
        'Contains approximately one trillion stars',
        'Will collide with the Milky Way in about 4.5 billion years',
        'Visible to the naked eye on dark nights'
      ],
      imageUrl: 'assets/images/andromeda.webp',
    ),
  ];

  List<CelestialBody> get celestialBodies => [..._celestialBodies];

  CelestialBody getById(String id) {
    return _celestialBodies.firstWhere((body) => body.id == id);
  }
}
