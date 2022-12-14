import React from "react";

function PanelExtraction({ layersVisible, setLayersVisible }) {
  const NumberIndicator = ({ children }) => (
    <div className="bg-emerald-600 text-white text-xl rounded-full p-2 w-10 h-10 flex justify-center items-center">
      {children}
    </div>
  );

  const handleLayerSelect = (layer) => () => {
    setLayersVisible({ ...layersVisible, [layer]: !layersVisible[layer] });
  };

  return (
    <section className="fixed z-20 right-10 bottom-20 p-4 bg-white">
      <h2 className="text-2xl my-2">To get stuff on SARTopo, do this:</h2>
      <div className="flex flex-row items-center my-2">
        <NumberIndicator>1</NumberIndicator>
        <span className="ml-2 text-xl">Pan to Area of Interest</span>
      </div>
      <div className="flex flex-row items-center my-2">
        <NumberIndicator>2</NumberIndicator>
        <span className="ml-2 text-xl">Select Datasets</span>
      </div>
      <div className="ml-12 select-none">
        <div className="flex flex-row">
          <input
            type="checkbox"
            name=""
            id="layer1"
            className="mr-2"
            checked={layersVisible.shelters}
            onChange={handleLayerSelect("shelters")}
          />
          <label htmlFor="layer1">shelters</label>
        </div>
        <div className="flex flex-row">
          <input
            type="checkbox"
            name=""
            id="layer2"
            className="mr-2"
            checked={layersVisible.roads}
            onChange={handleLayerSelect("roads")}
          />
          <label htmlFor="layer2">roads</label>
        </div>
        <div className="flex flex-row">
          <input
            type="checkbox"
            name=""
            id="layer3"
            className="mr-2"
            checked={layersVisible.trails}
            onChange={handleLayerSelect("trails")}
          />
          <label htmlFor="layer3">trails</label>
        </div>
      </div>

      <div className="flex flex-row items-center my-2">
        <NumberIndicator>3</NumberIndicator>
        <span className="ml-2 text-xl">Download the data</span>
      </div>

      <div className="flex flex-row items-center my-2">
        <NumberIndicator>4</NumberIndicator>
        <span className="ml-2 text-xl">Import unzipped data into SAR Topo</span>
      </div>
    </section>
  );
}

export default PanelExtraction;
