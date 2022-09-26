import { useState } from "preact/hooks";
import ContactBadge from "./ContactBadge";
import Header from "./Header";
import ModalAuthentication from "./ModalAuthentication";
import MapInterface from "./MapInterface";
import PanelExtraction from "./PanelExtraction";

export function App() {
  const [authenticated, setAuthenticated] = useState(
    import.meta.env.VITE_IGNORE_AUTH ?? false
  );
  const [layersVisible, setLayersVisible] = useState({
    roads: true,
    trails: true,
    shelters: true,
  });
  const [mapBounds, setMapBounds] = useState(null);

  function onAuthenticate() {
    setAuthenticated(true);
  }

  return (
    <>
      <Header />
      <ContactBadge />

      <main className="h-screen">
        <MapInterface
          layersVisible={layersVisible}
          setMapBounds={setMapBounds}
        />
      </main>

      {authenticated ? (
        <PanelExtraction
          layersVisible={layersVisible}
          setLayersVisible={setLayersVisible}
        />
      ) : (
        <ModalAuthentication handleAuthenticated={onAuthenticate} />
      )}
    </>
  );
}

export default App;
