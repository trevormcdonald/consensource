'use strict'

const m = require('mithril')
const authService = require('App/services/auth')
const agentService = require('App/services/agent')
const modals = require('App/components/modals')
const { AuthedComponent } = require('App/views/common/auth')


const _navLink = (route, asset_active, asset_inactive, label) =>
  m('li.nav-item.retailer_nav',

  m(`a.nav-link.retailer_nav_link[href=${route}]`,
    {class: m.route.get() === route ? 'active' : '', oncreate: m.route.link},
    [ m(`img.nav_icon[src=/assets/images/${m.route.get() === route ? asset_active : asset_inactive}]`), m('span.nav_label.p-1.ml-1', label)]))

const _authButtons = () => {
  if (authService.isSignedIn()) {
    return  m('li.nav-item',
            m(`a.nav-link[href=/index_factory.html].retailer_nav_link#sign_out`,  {onclick: () => {
                 authService.clear()
                 m.route.set('/')
               } }, m('img.nav_icon.mr-1[src=/assets/images/logout-icon.svg]'),'Log Out'))


  } else {
    return [
      m('a.btn.btn-outline-success[href=/signIn]', { oncreate: m.route.link }, 'Sign In'),
      m('a.btn.btn-link.small.text-muted[href=/signUp]', { oncreate: m.route.link }, 'Not a member? Sign Up')
    ]
  }
}

const _greeting = (vnode) => {
    if (vnode.state.agent) {
        return m(AuthedComponent, `Hi, ${vnode.state.agent.name}`)
    }
    return  `Welcome`
}

const _getAgentData = (vnode) => authService.getUserData()
      .then((user) => Promise.all([agentService.fetchAgent(user.public_key)])
      .then(([agent]) => {
         vnode.state.agent = agent.data
         vnode.state.loading = false
         m.redraw()
      })
      .catch((e) => {
        console.log(e)
        vnode.state.loading = false
      }))

const App = {
  _viewName: 'App',
  oninit: (vnode) => {
    vnode.state.agent = null
    vnode.state.loading = false

  },
  onupdate: (vnode) => {
    if (authService.isSignedIn() &&  vnode.state.agent === null && vnode.state.loading === false) {
        _getAgentData(vnode)
    }
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
              m('span.logo-circle', m('img.mt-1.org-logo[src="/assets/images/Stora_Enso.svg"].d-inline-block.align-top')),
            ]),
            m('span.ml-3.greeting_text', _greeting(vnode)),
            m('div.collapse.navbar-collapse', [
              m('ul.navbar-nav.ml-auto',
                [
                  m(AuthedComponent, _navLink('/requests','certified-factories-icon.svg', 'inactive-cert-factories.svg' ,'Request Certification')),
                  m(AuthedComponent, _navLink('/profile', 'active-profile.svg', 'profile-icon.svg' ,'Profile')),
                  _authButtons()
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
      m('p', ['Welcome to Consensource Auditor'])
    ],
}
module.exports = {
  App, Welcome
}
