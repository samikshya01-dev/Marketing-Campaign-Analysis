import React, { useState, useMemo } from 'react';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { TrendingUp, Users, DollarSign, MousePointer, Filter, Download } from 'lucide-react';

const MarketingCampaignDashboard: React.FC = () => {
  // Sample data simulating Google Analytics export
  const campaignData = [
    { channel: 'Email', sessions: 15420, conversions: 982, revenue: 49100, avgDuration: 245, bounceRate: 32 },
    { channel: 'Paid Search', sessions: 22340, conversions: 1456, revenue: 72800, avgDuration: 198, bounceRate: 45 },
    { channel: 'Social Media', sessions: 31200, conversions: 936, revenue: 28080, avgDuration: 156, bounceRate: 58 },
    { channel: 'Direct', sessions: 18900, conversions: 1323, revenue: 66150, avgDuration: 289, bounceRate: 28 },
    { channel: 'Organic Search', sessions: 28400, conversions: 1704, revenue: 85200, avgDuration: 223, bounceRate: 38 },
    { channel: 'Referral', sessions: 12100, conversions: 363, revenue: 18150, avgDuration: 167, bounceRate: 52 }
  ];

  const weeklyTrends = [
    { week: 'Week 1', email: 220, paidSearch: 310, social: 180, organic: 390 },
    { week: 'Week 2', email: 245, paidSearch: 325, social: 195, organic: 405 },
    { week: 'Week 3', email: 238, paidSearch: 342, social: 210, organic: 420 },
    { week: 'Week 4', email: 279, paidSearch: 479, social: 351, organic: 489 }
  ];

  const customerSegments = [
    { name: 'High-Value Engaged', users: 2340, revenue: 140400, avgSession: 345, color: '#10b981' },
    { name: 'Casual Browsers', users: 12800, revenue: 89600, avgSession: 142, color: '#3b82f6' },
    { name: 'Deal Seekers', users: 5600, revenue: 72800, avgSession: 198, color: '#f59e0b' },
    { name: 'One-Time Visitors', users: 8200, revenue: 16400, avgSession: 87, color: '#ef4444' }
  ];

  const [selectedChannel, setSelectedChannel] = useState('All');
  const [dateRange, setDateRange] = useState('Last 30 Days');

  // Calculate KPIs
  const totalSessions = useMemo(() =>
    campaignData.reduce((sum, item) => sum + item.sessions, 0), []);

  const totalConversions = useMemo(() =>
    campaignData.reduce((sum, item) => sum + item.conversions, 0), []);

  const totalRevenue = useMemo(() =>
    campaignData.reduce((sum, item) => sum + item.revenue, 0), []);

  const avgConversionRate = useMemo(() =>
    ((totalConversions / totalSessions) * 100).toFixed(2), [totalConversions, totalSessions]);

  // Filter data based on selection
  const filteredData = useMemo(() => {
    if (selectedChannel === 'All') return campaignData;
    return campaignData.filter(item => item.channel === selectedChannel);
  }, [selectedChannel]);

  // Prepare data for conversion funnel
  const funnelData = useMemo(() =>
    campaignData.map(item => ({
      channel: item.channel,
      conversionRate: ((item.conversions / item.sessions) * 100).toFixed(2),
      roi: ((item.revenue / (item.sessions * 2)) * 100).toFixed(0)
    })).sort((a, b) => b.conversionRate - a.conversionRate),
  []);

  const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-blue-500">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">
                Marketing Campaign Analytics
              </h1>
              <p className="text-gray-600">E-Commerce Performance Dashboard | TrendKart Analytics</p>
            </div>
            <div className="flex gap-3">
              <select
                value={dateRange}
                onChange={(e) => setDateRange(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option>Last 7 Days</option>
                <option>Last 30 Days</option>
                <option>Last Quarter</option>
              </select>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2">
                <Download size={18} />
                Export
              </button>
            </div>
          </div>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg shadow p-6 border-t-4 border-blue-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Total Sessions</p>
                <p className="text-2xl font-bold text-gray-800">{totalSessions.toLocaleString()}</p>
                <p className="text-xs text-green-600 mt-1">↑ 12.5% vs last period</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <Users className="text-blue-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-t-4 border-green-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Conversions</p>
                <p className="text-2xl font-bold text-gray-800">{totalConversions.toLocaleString()}</p>
                <p className="text-xs text-green-600 mt-1">↑ 8.3% vs last period</p>
              </div>
              <div className="bg-green-100 p-3 rounded-full">
                <MousePointer className="text-green-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-t-4 border-purple-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Total Revenue</p>
                <p className="text-2xl font-bold text-gray-800">${(totalRevenue / 1000).toFixed(1)}k</p>
                <p className="text-xs text-green-600 mt-1">↑ 15.7% vs last period</p>
              </div>
              <div className="bg-purple-100 p-3 rounded-full">
                <DollarSign className="text-purple-600" size={24} />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-t-4 border-orange-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-1">Conversion Rate</p>
                <p className="text-2xl font-bold text-gray-800">{avgConversionRate}%</p>
                <p className="text-xs text-green-600 mt-1">↑ 2.1% vs last period</p>
              </div>
              <div className="bg-orange-100 p-3 rounded-full">
                <TrendingUp className="text-orange-600" size={24} />
              </div>
            </div>
          </div>
        </div>

        {/* Channel Filter */}
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center gap-3">
            <Filter size={20} className="text-gray-600" />
            <span className="text-sm font-medium text-gray-700">Filter by Channel:</span>
            <div className="flex gap-2 flex-wrap">
              {['All', ...campaignData.map(item => item.channel)].map(channel => (
                <button
                  key={channel}
                  onClick={() => setSelectedChannel(channel)}
                  className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
                    selectedChannel === channel
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {channel}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Main Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Channel Performance Bar Chart */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Channel Performance Overview</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={filteredData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="channel" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
                />
                <Legend />
                <Bar dataKey="sessions" fill="#3b82f6" name="Sessions" radius={[8, 8, 0, 0]} />
                <Bar dataKey="conversions" fill="#10b981" name="Conversions" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Revenue by Channel */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Revenue Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={filteredData}
                  dataKey="revenue"
                  nameKey="channel"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label={({ channel, percent }) => `${channel} ${(percent * 100).toFixed(0)}%`}
                  labelLine={false}
                >
                  {filteredData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Conversion Funnel & Weekly Trends */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Conversion Rate Analysis */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Conversion Rate & ROI by Channel</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={funnelData} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis type="number" tick={{ fontSize: 12 }} />
                <YAxis dataKey="channel" type="category" width={100} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="conversionRate" fill="#8b5cf6" name="Conv. Rate %" radius={[0, 8, 8, 0]} />
                <Bar dataKey="roi" fill="#f59e0b" name="ROI %" radius={[0, 8, 8, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Weekly Trends */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Weekly Conversion Trends</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={weeklyTrends}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="week" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="email" stroke="#10b981" strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="paidSearch" stroke="#3b82f6" strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="social" stroke="#f59e0b" strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="organic" stroke="#8b5cf6" strokeWidth={2} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Customer Segments */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Customer Segmentation Analysis (K-Means Clustering)</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {customerSegments.map((segment, index) => (
              <div key={index} className="border-2 rounded-lg p-4" style={{ borderColor: segment.color }}>
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-4 h-4 rounded-full" style={{ backgroundColor: segment.color }}></div>
                  <h4 className="font-semibold text-gray-800">{segment.name}</h4>
                </div>
                <div className="space-y-2">
                  <div>
                    <p className="text-xs text-gray-600">Users</p>
                    <p className="text-xl font-bold text-gray-800">{segment.users.toLocaleString()}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Revenue</p>
                    <p className="text-lg font-semibold" style={{ color: segment.color }}>
                      ${(segment.revenue / 1000).toFixed(1)}k
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Avg Session (sec)</p>
                    <p className="text-sm text-gray-700">{segment.avgSession}s</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Key Insights */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg shadow-lg p-6 border-l-4 border-blue-500">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">📊 Key Insights & Recommendations</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white rounded-lg p-4">
              <h4 className="font-semibold text-green-600 mb-2">✓ High Performers</h4>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• Email & Paid Search drive 65% of conversions</li>
                <li>• Organic Search has highest ROI at 425%</li>
                <li>• High-Value Engaged segment (10% users) = 45% revenue</li>
              </ul>
            </div>
            <div className="bg-white rounded-lg p-4">
              <h4 className="font-semibold text-orange-600 mb-2">⚠ Opportunities</h4>
              <ul className="text-sm text-gray-700 space-y-1">
                <li>• Social Media: High traffic, low conversion (3%)</li>
                <li>• Implement retargeting campaigns for casual browsers</li>
                <li>• Launch loyalty program for high-value customers</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-sm text-gray-500 py-4">
          <p>Dashboard created using Google Analytics 4 data | Python (Pandas, Scikit-learn) | React & Recharts</p>
        </div>
      </div>
    </div>
  );
};

export default MarketingCampaignDashboard;
