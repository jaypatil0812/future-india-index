import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer,
    PieChart, Pie, Cell
} from 'recharts';

function IndexOverview() {
    const [historyDays, setHistoryDays] = useState(30);
    const [overview, setOverview] = useState(null);
    const [history, setHistory] = useState([]);
    const [outperformance, setOutperformance] = useState(0);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Fetch overview
        axios.get(`${process.env.REACT_APP_API_URL}/index/overview`)
            .then(res => setOverview(res.data))
            .catch(err => {
                console.error("Failed to fetch abstract index overview:", err);
            });
    }, []);

    useEffect(() => {
        setLoading(true);
        axios.get(`${process.env.REACT_APP_API_URL}/index/history?days=${historyDays}`)
            .then(res => {
                setHistory(res.data.history);
                setOutperformance(res.data.outperformance);
            })
            .catch(err => {
                console.error("Failed to fetch history:", err);
            })
            .finally(() => setLoading(false));
    }, [historyDays]);

    const COLORS = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ec4899', '#64748b'];

    const CustomPieLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index, name }) => {
        const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
        const x = cx + radius * Math.cos(-midAngle * Math.PI / 180);
        const y = cy + radius * Math.sin(-midAngle * Math.PI / 180);

        return (
            <text x={x} y={y} fill="white" textAnchor="middle" dominantBaseline="central" fontSize={12} fontWeight="bold">
                {`${(percent * 100).toFixed(0)}%`}
            </text>
        );
    };

    return (
        <div style={{ padding: "16px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", marginBottom: "32px" }}>
                <div>
                    <h1 style={{ fontSize: "28px", fontWeight: "bold", margin: "0 0 8px 0", color: "#111827" }}>
                        ISTE Index
                    </h1>
                    <p style={{ color: "#6b7280", margin: 0 }}>
                        Tracking the next generation of Indian economic powerhouses.
                    </p>
                </div>

                {overview && (
                    <div style={{ textAlign: "right", background: "white", padding: "16px", borderRadius: "12px", border: "1px solid #e5e7eb", boxShadow: "0 4px 6px -1px rgba(0,0,0,0.05)" }}>
                        <div style={{ fontSize: "14px", color: "#6b7280", fontWeight: "600", marginBottom: "4px" }}>
                            INDEX VALUE
                        </div>
                        <div style={{ display: "flex", alignItems: "baseline", gap: "12px" }}>
                            <span style={{ fontSize: "32px", fontWeight: "bold", color: "#111827" }}>
                                {overview.index_value.toLocaleString()}
                            </span>
                            <span style={{
                                fontSize: "18px",
                                fontWeight: "bold",
                                color: overview.percent_change >= 0 ? "#10b981" : "#ef4444",
                                background: overview.percent_change >= 0 ? "#dcfce7" : "#fee2e2",
                                padding: "2px 8px",
                                borderRadius: "8px"
                            }}>
                                {overview.percent_change >= 0 ? '▲' : '▼'} {Math.abs(overview.percent_change).toFixed(2)}%
                            </span>
                        </div>
                    </div>
                )}
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px", marginBottom: "24px" }}>

                {/* Sector Allocation Panel */}
                <div style={{ background: "white", borderRadius: "16px", padding: "24px", border: "1px solid #e5e7eb", boxShadow: "0 4px 6px -1px rgba(0,0,0,0.05)" }}>
                    <h2 style={{ fontSize: "18px", fontWeight: "bold", marginBottom: "16px", color: "#111827", display: "flex", alignItems: "center", gap: "8px" }}>
                        Sector Allocation
                    </h2>
                    <div style={{ height: "300px", position: "relative" }}>
                        {overview ? (
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={overview.allocations}
                                        cx="50%"
                                        cy="50%"
                                        labelLine={false}
                                        label={CustomPieLabel}
                                        outerRadius={120}
                                        innerRadius={60}
                                        fill="#8884d8"
                                        dataKey="value"
                                        stroke="none"
                                    >
                                        {overview.allocations.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <RechartsTooltip formatter={(value) => `${value.toFixed(1)}%`} />
                                    <Legend layout="vertical" verticalAlign="middle" align="right" />
                                </PieChart>
                            </ResponsiveContainer>
                        ) : (
                            <div style={{ display: "flex", height: "100%", justifyContent: "center", alignItems: "center", color: "#6b7280" }}>Loading...</div>
                        )}
                    </div>
                </div>

                {/* Benchmark Outperformance */}
                <div style={{ background: "white", borderRadius: "16px", padding: "24px", border: "1px solid #e5e7eb", boxShadow: "0 4px 6px -1px rgba(0,0,0,0.05)" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
                        <h2 style={{ fontSize: "18px", fontWeight: "bold", color: "#111827", display: "flex", alignItems: "center", gap: "8px", margin: 0 }}>
                            VS Nifty 50
                        </h2>
                        <div style={{ display: "flex", gap: "8px" }}>
                            {[7, 30, 90, 365].map(d => (
                                <button
                                    key={d}
                                    onClick={() => setHistoryDays(d)}
                                    style={{
                                        padding: "4px 12px",
                                        borderRadius: "16px",
                                        border: "none",
                                        background: historyDays === d ? "#3b82f6" : "#f1f5f9",
                                        color: historyDays === d ? "white" : "#64748b",
                                        fontSize: "12px",
                                        fontWeight: "bold",
                                        cursor: "pointer"
                                    }}
                                >
                                    {d === 365 ? '1Y' : `${d}D`}
                                </button>
                            ))}
                        </div>
                    </div>

                    <div style={{ marginBottom: "16px", display: "flex", alignItems: "center", gap: "12px" }}>
                        <span style={{ fontSize: "14px", color: "#64748b" }}>vs Alpha Outperformance:</span>
                        <span style={{
                            fontSize: "20px",
                            fontWeight: "bold",
                            color: outperformance >= 0 ? "#10b981" : "#ef4444"
                        }}>
                            {outperformance >= 0 ? '+' : ''}{outperformance.toFixed(2)}%
                        </span>
                    </div>

                    <div style={{ height: "240px" }}>
                        {loading ? (
                            <div style={{ display: "flex", height: "100%", justifyContent: "center", alignItems: "center", color: "#6b7280" }}>Loading charts...</div>
                        ) : (
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={history} margin={{ top: 5, right: 10, left: 10, bottom: 5 }}>
                                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                                    <XAxis dataKey="date" tick={{ fontSize: 10 }} tickFormatter={(val) => val.substring(5)} minTickGap={30} />
                                    <YAxis yAxisId="left" domain={['auto', 'auto']} stroke="#3b82f6" tick={{ fontSize: 10 }} hide />
                                    <YAxis yAxisId="right" orientation="right" domain={['auto', 'auto']} stroke="#64748b" tick={{ fontSize: 10 }} hide />
                                    <RechartsTooltip
                                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                                    />
                                    <Legend iconType="circle" />
                                    <Line yAxisId="left" type="monotone" dataKey="future_india" name="ISTE Index" stroke="#3b82f6" strokeWidth={3} dot={false} activeDot={{ r: 6 }} />
                                    <Line yAxisId="right" type="monotone" dataKey="nifty_50" name="Nifty 50 (^NSEI)" stroke="#94a3b8" strokeWidth={2} dot={false} strokeDasharray="5 5" />
                                </LineChart>
                            </ResponsiveContainer>
                        )}
                    </div>
                </div>

            </div>
        </div>
    );
}

export default IndexOverview;
