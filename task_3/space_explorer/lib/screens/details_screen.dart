import 'package:flutter/material.dart';
import '../models/celestial_body.dart';
import 'package:flutter_animate/flutter_animate.dart';

class DetailsScreen extends StatelessWidget {
  final CelestialBody celestialBody;

  const DetailsScreen({
    super.key,
    required this.celestialBody,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.background,
      appBar: AppBar(
        title: Text(celestialBody.name),
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Displaying the image (Network or Asset)
            Container(
              height: 250,
              width: double.infinity,
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.surface,
                image: celestialBody.imageUrl.startsWith('http')
                    ? DecorationImage(
                        image: NetworkImage(celestialBody.imageUrl),
                        fit: BoxFit.cover,
                      )
                    : DecorationImage(
                        image: AssetImage(celestialBody.imageUrl),
                        fit: BoxFit.cover,
                      ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    celestialBody.type,
                    style: TextStyle(
                      color: Theme.of(context).colorScheme.secondary,
                      fontSize: 16,
                    ),
                  ).animate().fadeIn().slideX(),
                  const SizedBox(height: 8),
                  Text(
                    celestialBody.description,
                    style: const TextStyle(fontSize: 18),
                  ).animate().fadeIn().slideX(),
                  const SizedBox(height: 24),
                  _buildInfoSection(
                    context,
                    'Size',
                    celestialBody.size,
                  ),
                  _buildInfoSection(
                    context,
                    'Distance from Earth',
                    celestialBody.distanceFromEarth,
                  ),
                  const SizedBox(height: 24),
                  Text(
                    'Interesting Facts',
                    style: Theme.of(context).textTheme.titleLarge,
                  ).animate().fadeIn().slideX(),
                  const SizedBox(height: 16),
                  ...celestialBody.facts.map((fact) => _buildFactItem(fact)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoSection(BuildContext context, String title, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 4),
          Text(
            value,
            style: const TextStyle(fontSize: 16),
          ),
        ],
      ),
    ).animate().fadeIn().slideX();
  }

  Widget _buildFactItem(String fact) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Padding(
            padding: EdgeInsets.only(top: 6),
            child: Icon(
              Icons.star,
              size: 16,
              color: Colors.amber,
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              fact,
              style: const TextStyle(fontSize: 16),
            ),
          ),
        ],
      ),
    ).animate().fadeIn().slideX();
  }
}
