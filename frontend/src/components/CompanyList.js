import React, { useState } from "react";

function CompanyList({ companies, onSelect, selectedCompany }) {
  const [expandedSectors, setExpandedSectors] = useState({
    "AI & Cloud": true,
    "Semiconductors": true,
    "Clean Energy": false,
    "EV & Battery": false,
    "Biotech": false,
    "Defense": false
  });

  const toggleSector = (sector) => {
    setExpandedSectors(prev => ({
      ...prev,
      [sector]: !prev[sector]
    }));
  };

  // Group companies by sector
  const sectors = companies.reduce((acc, company) => {
    if (!acc[company.sector]) {
      acc[company.sector] = [];
    }
    acc[company.sector].push(company);
    return acc;
  }, {});

  const getHealthColor = (status) => {
    if (status === 'green') return '#10b981'; // Green
    if (status === 'yellow') return '#f59e0b'; // Yellow
    if (status === 'red') return '#ef4444'; // Red
    return '#9ca3af';
  };

  return (
    <div style={{ padding: "0" }}>
      <button 
        onClick={() => onSelect(null)}
        style={{
          width: "100%",
          padding: "12px 16px",
          background: !selectedCompany ? "#eff6ff" : "transparent",
          border: "none",
          borderBottom: "1px solid #e5e7eb",
          textAlign: "left",
          fontSize: "16px",
          fontWeight: !selectedCompany ? "bold" : "normal",
          color: !selectedCompany ? "#1d4ed8" : "#374151",
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          gap: "8px"
        }}
      >
        ISTE Index Home
      </button>

      {Object.entries(sectors).map(([sectorName, sectorCompanies]) => (
        <div key={sectorName} style={{ borderBottom: "1px solid #f3f4f6" }}>
          <button
            onClick={() => toggleSector(sectorName)}
            style={{
              width: "100%",
              padding: "12px 16px",
              background: "#f9fafb",
              border: "none",
              textAlign: "left",
              fontWeight: "600",
              color: "#4b5563",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              cursor: "pointer"
            }}
          >
            <span>
              {expandedSectors[sectorName] ? '▼' : '▶'} {sectorName}
            </span>
            <span style={{ fontSize: "12px", background: "#e5e7eb", padding: "2px 8px", borderRadius: "12px" }}>
              {sectorCompanies.length}
            </span>
          </button>
          
          {expandedSectors[sectorName] && (
            <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
              {sectorCompanies.map((c) => (
                <li
                  key={c.id}
                  style={{ 
                    padding: "10px 16px 10px 32px",
                    cursor: "pointer", 
                    background: selectedCompany === c.symbol ? "#eff6ff" : "white",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    borderLeft: selectedCompany === c.symbol ? "4px solid #3b82f6" : "4px solid transparent",
                    transition: "all 0.2s"
                  }}
                  onClick={() => onSelect(c.symbol)}
                  onMouseOver={(e) => {
                    if (selectedCompany !== c.symbol) e.currentTarget.style.background = "#f3f4f6";
                  }}
                  onMouseOut={(e) => {
                    if (selectedCompany !== c.symbol) e.currentTarget.style.background = "white";
                  }}
                >
                  <div>
                    <div style={{ 
                      fontWeight: selectedCompany === c.symbol ? "600" : "500",
                      color: selectedCompany === c.symbol ? "#1d4ed8" : "#111827",
                      fontSize: "14px"
                    }}>
                      {c.name}
                    </div>
                    <div style={{ fontSize: "12px", color: "#6b7280" }}>{c.symbol}</div>
                  </div>
                  
                  {/* Health Badge */}
                  <div 
                    title={`Health Check: ${c.health?.status || 'Unknown'}`}
                    style={{
                      width: "12px",
                      height: "12px",
                      borderRadius: "50%",
                      background: getHealthColor(c.health?.status)
                    }}
                  />
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  );
}

export default CompanyList;
