import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StockChart from './StockChart';

function StockDetail({ companySymbol, companyData, allCompanies }) {
    const [stockData, setStockData] = useState([]);
    const [days, setDays] = useState(30);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (companySymbol) {
            setLoading(true);
            axios.get(`${process.env.REACT_APP_API_URL}/stocks/company/${companySymbol}?days=${days}`, {
                headers: {
                    'Bypass-Tunnel-Reminder': 'true'
                }
            })
                .then((res) => {
                    console.log("Stock details response:", res.data);
                    if (!res.data.error && Array.isArray(res.data) && res.data.length > 0) {
                        setStockData(res.data);
                    } else {
                        setStockData([]);
                    }
                })
                .catch((err) => {
                    console.error("Stock fetch error:", err);
                    setStockData([]);
                })
                .finally(() => setLoading(false));
        }
    }, [companySymbol, days]);

    if (!companyData) return null;

    const { score, health, sector_weight, sector } = companyData;
    const sectorPeers = allCompanies.filter(c => c.sector === sector).sort((a, b) => b.score.total_score - a.score.total_score);

    const ProgressBar = ({ label, value, color }) => (
        <div style={{ marginBottom: "12px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", fontWeight: "600", marginBottom: "4px", color: "#4b5563" }}>
                <span>{label}</span>
                <span>{value}%</span>
            </div>
            <div style={{ height: "6px", background: "#f3f4f6", borderRadius: "3px", overflow: "hidden" }}>
                <div style={{ height: "100%", width: `${value}%`, background: color, borderRadius: "3px", transition: "width 0.5s ease" }} />
            </div>
        </div>
    );

    return (
        <div style={{ padding: "0 16px 32px" }}>
            {/* Top Header Section */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "24px" }}>
                <div>
                    <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "8px" }}>
                        <h1 style={{ fontSize: "32px", fontWeight: "bold", margin: 0, color: "#111827" }}>
                            {companyData.name}
                        </h1>
                        <span style={{ background: "#e0e7ff", color: "#3730a3", padding: "4px 12px", borderRadius: "16px", fontSize: "14px", fontWeight: "bold" }}>
                            {companyData.symbol}
                        </span>
                    </div>
                    <div style={{ color: "#6b7280", fontWeight: "500" }}>Sector: {companyData.sector}</div>
                </div>

                {/* Final Stock Score Badge */}
                <div style={{
                    background: "linear-gradient(135deg, #3b82f6, #4f46e5)",
                    padding: "16px 24px",
                    borderRadius: "16px",
                    color: "white",
                    boxShadow: "0 10px 15px -3px rgba(59, 130, 246, 0.3)",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center"
                }}>
                    <div style={{ fontSize: "14px", opacity: 0.9, fontWeight: "600" }}>FUTURE INDIA SCORE</div>
                    <div style={{ fontSize: "42px", fontWeight: "bold", lineHeight: 1 }}>
                        {score.total_score}
                    </div>
                    <div style={{ fontSize: "12px", opacity: 0.8 }}>/ 100 pt max</div>
                </div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px", marginBottom: "32px" }}>

                {/* Scoring Engine Breakdown */}
                <div style={{ background: "white", borderRadius: "16px", padding: "24px", border: "1px solid #e5e7eb" }}>
                    <h2 style={{ fontSize: "18px", fontWeight: "bold", marginBottom: "20px", color: "#111827", display: "flex", alignItems: "center", gap: "8px" }}>
                        <span>🎯</span> Engine Component Breakdown
                    </h2>

                    <ProgressBar label="Growth Score (25% weight)" value={score.components.growth} color="#3b82f6" />
                    <ProgressBar label="Profitability Score (25% weight)" value={score.components.profitability} color="#10b981" />
                    <ProgressBar label="Quality Score (20% weight)" value={score.components.quality} color="#f59e0b" />
                    <ProgressBar label="Innovation Score (15% weight)" value={score.components.innovation} color="#8b5cf6" />
                    <ProgressBar label="Scale Score (15% weight)" value={score.components.scale} color="#ec4899" />
                </div>

                <div>
                    {/* Health Check Panel */}
                    <div style={{ background: "white", borderRadius: "16px", padding: "24px", border: `2px solid ${health.status === 'green' ? '#10b981' : health.status === 'yellow' ? '#f59e0b' : '#ef4444'}`, marginBottom: "24px" }}>
                        <h2 style={{ fontSize: "18px", fontWeight: "bold", marginBottom: "16px", color: "#111827", display: "flex", alignItems: "center", gap: "8px" }}>
                            <span>🩺</span> Health Check Checklist
                        </h2>
                        <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "12px" }}>
                            {health.criteria.map((c, i) => (
                                <li key={i} style={{ display: "flex", alignItems: "center", gap: "12px", fontSize: "15px", color: "#4b5563" }}>
                                    <span style={{
                                        display: "flex", alignItems: "center", justifyContent: "center",
                                        width: "24px", height: "24px", borderRadius: "50%",
                                        background: c.passed ? "#dcfce7" : "#fee2e2",
                                        color: c.passed ? "#16a34a" : "#dc2626",
                                        fontWeight: "bold", fontSize: "14px"
                                    }}>
                                        {c.passed ? "✓" : "✗"}
                                    </span>
                                    {c.name}
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* Weight Calculator Panel */}
                    <div style={{ background: "white", borderRadius: "16px", padding: "24px", border: "1px solid #e5e7eb" }}>
                        <h2 style={{ fontSize: "18px", fontWeight: "bold", marginBottom: "16px", color: "#111827", display: "flex", alignItems: "center", gap: "8px" }}>
                            <span>⚖️</span> Sector Target Allocator
                        </h2>
                        <div style={{ display: "flex", gap: "24px", marginBottom: "16px" }}>
                            <div>
                                <div style={{ fontSize: "12px", color: "#6b7280", fontWeight: "600" }}>INTRA-SECTOR WEIGHT</div>
                                <div style={{ fontSize: "24px", fontWeight: "bold", color: "#111827" }}>{sector_weight}%</div>
                            </div>
                        </div>

                        <div style={{ background: "#f8fafc", borderRadius: "8px", padding: "12px", border: "1px solid #e2e8f0" }}>
                            <div style={{ fontSize: "12px", fontWeight: "bold", color: "#64748b", display: "flex", justifyContent: "space-between", marginBottom: "8px", borderBottom: "1px solid #cbd5e1", paddingBottom: "4px" }}>
                                <span>Peer</span><span>Score</span><span>Weight</span>
                            </div>
                            {sectorPeers.map(p => (
                                <div key={p.id} style={{ display: "flex", justifyContent: "space-between", fontSize: "13px", color: p.id === companyData.id ? "#1d4ed8" : "#475569", fontWeight: p.id === companyData.id ? "700" : "500", marginTop: "4px" }}>
                                    <span>{p.name}</span>
                                    <span>{p.score.total_score}</span>
                                    <span>{p.sector_weight}%</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Historical Charting Placeholder existing logic */}
            <div style={{ background: "white", borderRadius: "16px", padding: "24px", border: "1px solid #e5e7eb" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
                    <h2 style={{ fontSize: "18px", fontWeight: "bold", margin: 0, color: "#111827" }}>Price Trend Data (YFinance)</h2>
                    <div style={{ display: "flex", gap: "8px" }}>
                        {[7, 30, 90, 180, 365].map((d) => (
                            <button
                                key={d}
                                onClick={() => setDays(d)}
                                style={{
                                    padding: "6px 12px", borderRadius: "8px", border: "none",
                                    background: days === d ? "#3b82f6" : "#f3f4f6",
                                    color: days === d ? "white" : "#6b7280",
                                    fontSize: "13px", fontWeight: "600", cursor: "pointer"
                                }}
                            >
                                {d === 365 ? '1Y' : `${d}D`}
                            </button>
                        ))}
                    </div>
                </div>

                {loading ? (
                    <div style={{ textAlign: "center", padding: "40px" }}>Loading chart data...</div>
                ) : stockData.length > 0 ? (
                    <div style={{ height: "350px", background: "#f9fafb", borderRadius: "8px", padding: "16px", border: "1px solid #f3f4f6" }}>
                        <StockChart stockData={stockData} />
                    </div>
                ) : (
                    <div style={{ textAlign: "center", padding: "40px", color: "#9ca3af" }}>No recent price data available from Yahoo Finance.</div>
                )}
            </div>

        </div>
    );
}

export default StockDetail;
