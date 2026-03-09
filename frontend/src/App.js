import React, { useState, useEffect } from "react";
import axios from "axios";
import CompanyList from "./components/CompanyList";
import IndexOverview from "./components/IndexOverview";
import StockDetail from "./components/StockDetail";

function App() {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    axios.get(`${process.env.REACT_APP_API_URL}/companies`, {
      headers: { 'Bypass-Tunnel-Reminder': 'true' }
    })
      .then((res) => {
        setCompanies(res.data);
        setError(null);
      })
      .catch((err) => {
        console.error(err);
        setError("Failed to fetch companies");
      })
      .finally(() => setLoading(false));
  }, []);

  const styles = {
    container: {
      minHeight: '100vh',
      background: '#f8fafc',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    },
    header: {
      background: '#ffffff',
      boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
      borderBottom: '1px solid #e5e7eb',
      padding: '0 24px',
      position: 'sticky',
      top: 0,
      zIndex: 50
    },
    headerInner: {
      maxWidth: '1400px',
      margin: '0 auto',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      height: '72px'
    },
    logo: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px'
    },
    logoIcon: {
      width: '40px',
      height: '40px',
      background: 'linear-gradient(135deg, #10b981, #059669)',
      borderRadius: '8px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'white',
      fontSize: '20px',
      fontWeight: 'bold',
      boxShadow: '0 4px 6px -1px rgba(16, 185, 129, 0.4)'
    },
    logoText: {
      fontSize: '24px',
      fontWeight: '800',
      color: '#111827',
      letterSpacing: '-0.5px'
    },
    logoSubtext: {
      fontSize: '13px',
      color: '#64748b',
      marginTop: '2px',
      fontWeight: '500'
    },
    liveData: {
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      color: '#475569',
      fontSize: '14px',
      fontWeight: '600',
      background: '#f1f5f9',
      padding: '8px 16px',
      borderRadius: '20px'
    },
    mainContent: {
      maxWidth: '1400px',
      margin: '0 auto',
      padding: '24px',
      display: 'grid',
      gridTemplateColumns: '280px 1fr',
      gap: '24px',
      alignItems: 'start'
    },
    sidebar: {
      background: '#ffffff',
      borderRadius: '16px',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)',
      border: '1px solid #e2e8f0',
      overflow: 'hidden',
      position: 'sticky',
      top: '96px',
      maxHeight: 'calc(100vh - 120px)',
      display: 'flex',
      flexDirection: 'column'
    },
    sidebarHeader: {
      background: '#f8fafc',
      padding: '20px',
      borderBottom: '1px solid #e2e8f0'
    },
    sidebarTitle: {
      fontSize: '16px',
      fontWeight: '700',
      color: '#0f172a',
      marginBottom: '4px'
    },
    sidebarSubtitle: {
      fontSize: '13px',
      color: '#64748b',
      fontWeight: '500'
    },
    sidebarContent: {
      overflowY: 'auto',
      flex: 1
    },
    contentArea: {
      background: '#ffffff',
      borderRadius: '16px',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)',
      border: '1px solid #e2e8f0',
      minHeight: 'calc(100vh - 168px)'
    },
    spinnerArea: {
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100%',
      padding: '48px',
      color: '#64748b',
      fontWeight: '500'
    }
  };

  const selectedCompanyData = companies.find(c => c.symbol === selectedCompany);

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <div style={styles.headerInner}>
          <div style={styles.logo}>
            <div style={styles.logoIcon}>🇮🇳</div>
            <div>
              <div style={styles.logoText}>Future India Index</div>
              <div style={styles.logoSubtext}>V1.0 Advanced Index Engine</div>
            </div>
          </div>
          <div style={styles.liveData}>
            <span style={{ color: '#10b981' }}>●</span> Live API Connected
          </div>
        </div>
      </header>

      <div style={styles.mainContent}>
        {/* Sidebar */}
        <div style={styles.sidebar}>
          <div style={styles.sidebarHeader}>
            <div style={styles.sidebarTitle}>Index Constituents</div>
            <div style={styles.sidebarSubtitle}>
              {companies.length} components · 6 sectors
            </div>
          </div>
          <div style={styles.sidebarContent}>
            {loading && companies.length === 0 ? (
              <div style={styles.spinnerArea}>Loading constituents...</div>
            ) : error ? (
              <div style={{ padding: '20px', color: '#ef4444', fontSize: '14px' }}>{error}</div>
            ) : (
              <CompanyList
                companies={companies}
                onSelect={setSelectedCompany}
                selectedCompany={selectedCompany}
              />
            )}
          </div>
        </div>

        {/* Main View Area */}
        <div style={styles.contentArea}>
          {!selectedCompany ? (
            <IndexOverview />
          ) : (
            <StockDetail
              companySymbol={selectedCompany}
              companyData={selectedCompanyData}
              allCompanies={companies}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;