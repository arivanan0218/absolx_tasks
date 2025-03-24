import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/space_provider.dart';
import '../widgets/celestial_body_card.dart';
import 'package:flutter_animate/flutter_animate.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.background,
      appBar: AppBar(
        title: const Text('Space Explorer'),
      ),
      body: Consumer<SpaceProvider>(
        builder: (context, spaceProvider, child) {
          final celestialBodies = spaceProvider.celestialBodies;
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: celestialBodies.length,
            itemBuilder: (context, index) {
              return Animate(
                effects: const [
                  FadeEffect(duration: Duration(milliseconds: 500)),
                  SlideEffect(
                    begin: Offset(0, 0.2),
                    end: Offset.zero,
                    duration: Duration(milliseconds: 500),
                  ),
                ],
                child: Padding(
                  padding: const EdgeInsets.only(bottom: 16),
                  child: CelestialBodyCard(
                    celestialBody: celestialBodies[index],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
