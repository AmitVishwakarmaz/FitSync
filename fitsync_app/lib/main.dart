import 'package:fitsync_app/onboarding_screen.dart';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';

void main() async {
  // Ensure Flutter's widgets are initialized before running the app
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize Firebase with platform-specific configurations
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  // Run the app
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'FitSync App', // Updated the title
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true, // Optional: Enable Material 3 for modern design
      ),
      home: const OnboardingScreen(), // Main screen of the app
    );
  }
}
