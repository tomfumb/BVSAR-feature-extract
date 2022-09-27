import React from "react";

function Header() {
  return (
    <header className="flex flex-row justify-between items-center py-4 px-2 bg-emerald-600 text-white relative z-30">
      <div className="flex flex-row justify-evenly items-center">
        <div className="rounded-full bg-white h-12 w-12 overflow-hidden">
          <img src="/sar-logo.png" />
        </div>
        <div className="ml-4">{import.meta.env.VITE_SAR_ORG_NAME}</div>
      </div>
      <div className="uppercase  font-semibold">
        trail and toponym extractor
      </div>
    </header>
  );
}

export default Header;
