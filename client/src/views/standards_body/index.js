'use strict'

const m = require('mithril')
const AuthService = require('App/services/auth')
const { AuthedComponent } = require('App/views/common/auth')

const _navLink = (route, label) =>
  m('li.nav-item',
    { class: m.route.get() === route ? 'active' : '' },
    m(`a.nav-link[href=${route}]`, { oncreate: m.route.link, }, label))

const _authButtons = () => {
  if (AuthService.isSignedIn()) {
    return m('button.btn.btn-outline-secondary',
             {
               onclick: () => {
                 AuthService.clear()
                 m.route.set('/')
               }
             },
             'Sign Out')
  } else {
    return [
      m('a.btn.btn-outline-success[href=/signIn]', { oncreate: m.route.link }, 'Sign In'),
      m('a.btn.btn-link.small.text-muted[href=/signUp]', { oncreate: m.route.link }, 'Not a member? Sign Up')
    ]
  }
}

const App = {
  _viewName: 'App',
  view: (vnode) => {
    if (vnode.state.loading) {
      return [m('.row', 'Loading...')]
    } else {
      return [
        m('nav.navbar.navbar-expand-md.navbar-dark.bg-dark',
          [
            m('a.navbar-brand[href=/]', { oncreate: m.route.link }, "StandardsBody"),
            m('div.collapse.navbar-collapse', [
              m('ul.navbar-nav.mr-auto',
                [
                  m(AuthedComponent, _navLink('/profile', 'My Profile')),
                  m(AuthedComponent, _navLink('/standardsCreate', 'New Standard')),
                  m(AuthedComponent, _navLink('/standardsList', 'View Standards')),
                  m(AuthedComponent, _navLink('/certifyingBodyList', 'View Certifying Bodies')),
                ]),
                m('.mt-2.mt-md-0', _authButtons())
              ])
          ]),
        m('main.container', { role: 'main' }, [vnode.children]),
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
