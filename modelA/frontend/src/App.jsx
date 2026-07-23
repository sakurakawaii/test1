import React, { useEffect, useState } from "react";

function App() {
  const [stockLevels, setStockLevels] = useState([]);

  useEffect(() => {
    fetch("/api/stock-levels")
      .then((res) => res.json())
      .then((data) => setStockLevels(data));
  }, []);

  return (
    <div className="dashboard">
      <h1>Warehouse Stock Dashboard</h1>
      <ul>
        {stockLevels.map((item) => (
          <li key={item.sku}>
            {item.sku}: {item.onHand} on hand
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
