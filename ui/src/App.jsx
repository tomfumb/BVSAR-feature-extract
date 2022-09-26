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
    layerOne: false,
    layerTwo: false,
    layerThree: false,
  });
  const [mapCenter, setMapCenter] = useState([]);

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
          setMapCenter={setMapCenter}
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
