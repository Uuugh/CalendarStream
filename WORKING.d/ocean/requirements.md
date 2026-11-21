# Ocean scene

The Product Owner's statement: "using dart/flutter, generate a locally hosted website with an ocean scene". Answers: Q1 a sky, a sun and animated waves, only the waves move; Q2 `flutter run -d web-server --web-port 8080`; Q3 folder `WORKING.d/ocean`; Q4 the values in OCN-06.

- **Wave band**: one filled sine-wave shape that reaches the bottom of the window.
- **Back to front**: from the horizon down the page; layer 0 is the back band, layer 2 the front band.

`| ID | status | statement | test | evidence (temporary) |`

| ID | status | statement | test | evidence (temporary) |
|---|---|---|---|---|
| OCN-01 | planned | The page fills the window: the top 60% is sky in the color in OCN-06 and the bottom 40% is sea. | test/ocean_test.dart: OCN-01 | — |
| OCN-02 | backlog | A sun, a filled circle of the radius and color in OCN-06, is shown 80% across and 20% down the window and does not move. | test/ocean_test.dart: OCN-02 | — |
| OCN-03 | backlog | Three wave bands are drawn over the sea, back to front, each a sine wave of the height and wavelength in OCN-06 and in the color in OCN-06 for its layer. | test/ocean_test.dart: OCN-03 | — |
| OCN-04 | backlog | Each wave band moves horizontally and continuously at the speed in OCN-06 for its layer. Nothing else in the scene moves. | test/ocean_test.dart: OCN-04 | — |
| OCN-05 | planned | The root widget is `OceanApp` in `lib/main.dart`, and `flutter run -d web-server --web-port 8080` serves the page at `http://localhost:8080`. | test/ocean_test.dart: OCN-05 | — |
| OCN-06 | planned | Values: sky `#87CEEB`; sun `#FFD84D`, radius 60 logical pixels; wave colors back to front `#2A7FBF`, `#1E6FA8`, `#155A8A`; wave height 8 to 16 logical pixels; wavelength 200 to 300 logical pixels; speed back to front 20, 40 and 60 logical pixels per second. | see OCN-01 | — |
| OCN-07 | planned | The sky, the sun, the sea and each wave band are widgets with the keys `ValueKey('sky')`, `ValueKey('sun')`, `ValueKey('sea')` and `ValueKey('wave-0')` to `ValueKey('wave-2')`, so a test can find them and read their position. | see OCN-01 | — |
