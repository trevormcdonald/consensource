'use strict'

const m = require('mithril')
const modals = require('App/components/modals')

const _navLink = (route, asset_active, asset_inactive, label) =>
  m('li.nav-item.retailer_nav',

  m(`a.nav-link.retailer_nav_link[href=${route}]`,
    {class: m.route.get().startsWith(route) ? 'active' : '', oncreate: m.route.link},
    [ m(`img.nav_icon[src=/assets/images/${m.route.get().startsWith(route) ? asset_active : asset_inactive}]`), m('span.nav_label.p-1.ml-1', label)]))


const _greeting = () =>
  'Welcome, Retail sourcing member!'

const App = {
  _viewName: 'App',
  oninit: (vnode) => {
    vnode.state.loading = false
  },
  view: (vnode) => {
    if (vnode.state.loading) {
      return [m('.row', 'Loading...')]
    } else {
      return [
        m('nav.navbar.navbar-expand-md.navbar-light.bg-light',
          [
            m('a.navbar-brand.org-brand.greeting_text[href=/]', { oncreate: m.route.link },
            [
              m('span.logo-circle', m('img.org-logo[src="/assets/images/tgt-logo-red-small.svg"].d-inline-block.align-top')),
            ]),
            m('span.ml-3.greeting_text', _greeting()),
            m('div.collapse.navbar-collapse', [
              m('ul.navbar-nav.ml-auto',
                [
                  _navLink('/certifications', 'certified-factories-icon.svg', 'inactive-cert-factories.svg', 'Certified Factories'),
                  _navLink('/agents', 'active-agents.svg', 'inactive-agents.svg', 'Agents'),
                ]),

          ])
          ]),
        m('main.container.mt-5', { role: 'main' }, [vnode.children]),
        m(modals.ModalContainer, { show: modals.displayModal() })
      ]
    }
  },

  subpage: (element) => ({
    onmatch: (_args, _requestedPath) => element,
    render: (vnode) => m(App, vnode)
  })
}

const Welcome = {
  _viewName: 'Welcome',
  view: () =>
    [
      m('p', [_greeting()])
    ],
}
module.exports = {
  App, Welcome
}
