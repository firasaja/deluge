/*
Script: Deluge.Details.Peers.js
    The peers tab displayed in the details panel.

Copyright:
	(C) Damien Churchill 2009 <damoxc@gmail.com>
	This program is free software; you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation; either version 3, or (at your option)
	any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, write to:
		The Free Software Foundation, Inc.,
		51 Franklin Street, Fifth Floor
		Boston, MA  02110-1301, USA.
*/

(function() {
	function flagRenderer(value) {
		return String.format('<img src="/flag/{0}" />', value);
	}
	function peerAddressRenderer(value, p, record) {
		var seed = (record.data['seed'] == 1024) ? 'x-deluge-seed' : 'x-deluge-peer'
		return String.format('<div class="{0}">{1}</div>', seed, value);
	}
	function peerProgressRenderer(value) {
		var progress = (value * 100).toFixed(0);
		var width = new Number(this.style.match(/\w+:\s*(\d+)\w+/)[1]).toFixed(0) - 8;
		return Deluge.progressBar(progress, width, progress + '%');
	}
	function sort_address(value) {
		var m = value.match(/(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\:(\d+)/);
		var address = 0;
		var parts = [m[1], m[2], m[3], m[4]];
		Ext.each(parts, function(part, index) {
			part = parseInt(part);
			address = address | part << ((3 - index) * 8);
			//alert("Total: " + address + "\nPart: " + part + "\nIndex: " + index + "\nCalc: " + (part << ((3 - index) * 8)));
		});
		return address;
	}

	Ext.deluge.details.PeersTab = Ext.extend(Ext.grid.GridPanel, {
		
		constructor: function(config) {
			config = Ext.apply({
				title: _('Peers'),
				cls: 'x-deluge-peers',
				store: new Ext.data.SimpleStore({
					fields: [
						{name: 'country'},
						{name: 'address', sortType: sort_address},
						{name: 'client'},
						{name: 'progress', type: 'float'},
						{name: 'downspeed', type: 'int'},
						{name: 'upspeed', type: 'int'},
						{name: 'seed', type: 'int'}
					],
					id: 0
				}),
				columns: [{
					header: '&nbsp;',
					width: 30,
					sortable: true,
					renderer: flagRenderer,
					dataIndex: 'country'
				}, {
					header: 'Address',
					width: 125,
					sortable: true,
					renderer: peerAddressRenderer,
					dataIndex: 'address'
				}, {
					header: 'Client',
					width: 125,
					sortable: true,
					renderer: fplain,
					dataIndex: 'client'
				}, {
					header: 'Progress',
					width: 150,
					sortable: true,
					renderer: peerProgressRenderer,
					dataIndex: 'progress'
				}, {
					header: 'Down Speed',
					width: 100,
					sortable: true,
					renderer: fspeed,
					dataIndex: 'downspeed'
				}, {
					header: 'Up Speed',
					width: 100,
					sortable: true,
					renderer: fspeed,
					dataIndex: 'upspeed'
				}],	
				stripeRows: true,
				deferredRender:false,
				autoScroll:true
			}, config);
			Ext.deluge.details.PeersTab.superclass.constructor.call(this, config);
		},
		
		onRender: function(ct, position) {
			Ext.deluge.details.PeersTab.superclass.onRender.call(this, ct, position);
		},
		
		clear: function() {
			this.getStore().loadData([]);
		},
		
		update: function(torrentId) {
			Deluge.Client.core.get_torrent_status(torrentId, Deluge.Keys.Peers, {
				success: this.onRequestComplete,
				scope: this
			});
		},
		
		onRequestComplete: function(torrent, options) {
			var peers = new Array();
			Ext.each(torrent.peers, function(peer) {
				peers.push([peer.country, peer.ip, peer.client, peer.progress, peer.down_speed, peer.up_speed, peer.seed]);
			}, this);
			this.getStore().loadData(peers);
		}
	});
	Deluge.Details.add(new Ext.deluge.details.PeersTab());
})();