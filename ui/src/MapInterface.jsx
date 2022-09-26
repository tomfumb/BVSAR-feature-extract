import { useEffect, useRef } from "preact/hooks";

import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

import { generic } from "flatgeobuf";

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_GL_MAP;

// TOM: CHANGE THIS URL ENDPOINT
const roadSegments =
  "https://brian-search-rescue-test-bucket.s3.amazonaws.com/line-road-segments.fgb";

const shelterPoints =
  "https://brian-search-rescue-test-bucket.s3.amazonaws.com/point-shelters.fgb";
const trailSegments =
  "https://brian-search-rescue-test-bucket.s3.amazonaws.com/point-trails.fgb";

/** It's the map. Standard mapbox/maplibre setup with a possible addition of stuff? */
function MapInterface({ setMapCenter, layersVisible }) {
  const mapRef = useRef(null);

  // optionally show some meta-data about the FGB file
  function handleHeaderMeta(headerMeta) {
    const header = document.getElementById("header");
    const formatter = new JSONFormatter(headerMeta, 10);
    header.appendChild(formatter.render());
  }

  useEffect(() => {
    const center = import.meta.env.VITE_MAP_INIT_CENTER.split(",") ?? [0, 0];
    const zoom = import.meta.env.VITE_MAP_INIT_ZOOM ?? 4;

    mapRef.current = new mapboxgl.Map({
      container: mapRef.current,
      style: "mapbox://styles/mapbox/satellite-streets-v11",
      center, // starting position
      zoom, // starting zoom
    });

    const map = mapRef.current;

    if (import.meta.env.MODE === "development") {
      window.map = map;
    }

    map.on("moveend", async (e) => {
      const mapBounds = {
        minX: map.getBounds().getNorthWest().lng,
        minY: map.getBounds().getSouthEast().lat,
        maxX: map.getBounds().getSouthEast().lng,
        maxY: map.getBounds().getNorthWest().lat,
      };

      console.log("Typeof minX", typeof mapBounds.minX);

      const iterable = generic.deserialize(
        roadSegments,
        mapBounds,
        handleHeaderMeta
      );

      const fc = { features: [] };

      for await (let feature of iterable) {
        fc.features.push({ ...feature, id: i });
        i += 1;
      }

      console.log("Fc ", fc);
    });

    return () => {
      mapRef.current = null;
    };
  }, []);

  return <div className="w-full h-full" ref={mapRef} />;
}

export default MapInterface;
