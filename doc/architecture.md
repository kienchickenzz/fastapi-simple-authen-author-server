---
Kiến trúc mới

┌─────────────────────────────────────────────────────────────────┐
│                    Initializer (Base)                           │
│                    src/base/initializer.py                      │
│                                                                 │
│  - Setup app (version, debug)                                   │
│  - Validate OpenAPI                                             │
│  - Validate endpoints                                           │
│  - Khởi tạo EngineFactory                                       │
│  - Return State(config)                                         │
└─────────────────────────────────────────────────────────────────┘
                            ▲
                            │ extends
                            │
┌─────────────────────────────────────────────────────────────────┐
│                    AppInitializer                               │
│                    src/initializer.py                           │
│                                                                 │
│  async def __aenter__(self):                                    │
│      state = await super().__aenter__()  # Gọi lớp cha          │
│      db_engine = self.engine_factory.create_engine("DB")        │
│                                                                 │
│      # Gọi từng module đăng ký dependencies                     │
│      context = ModuleContext(db_engine, config)                 │
│      for module in modules:                                     │
│          deps = await module.initialize(context)                │
│          all_services.update(deps.services)                     │
│                                                                 │
│      return AppState(**state, **all_services, **all_repos)      │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ orchestrates
                             ▼
    ┌────────────────────────┼────────────────────────┐
    │                        │                        │
    ▼                        ▼                        ▼
┌──────────┐             ┌──────────┐            ┌──────────┐
│  User    │             │  Auth    │            │  Book    │  ...
│  Module  │             │  Module  │            │  Module  │
└──────────┘             └──────────┘            └──────────┘

---

Flow khởi tạo

App Start
    │
    ▼
AppInitializer.__aenter__()
    │
    ├── await super().__aenter__()  ──────────────────┐
    │                                                  │
    │   ┌──────────────────────────────────────────────┘
    │   │  Initializer.__aenter__()
    │   │    ├── _setup_app()
    │   │    ├── _validate_openapi()
    │   │    ├── _validate_endpoints()
    │   │    ├── engine_factory.__aenter__()
    │   │    └── return State(config)
    │   └──────────────────────────────────────────────┐
    │                                                  │
    ├── state = <result>  ◄────────────────────────────┘
    │
    ├── db_engine = engine_factory.create_engine("DB")
    │
    ├── context = ModuleContext(db_engine, config, {})
    │
    ├── UserModule.initialize(context)
    │     └── returns {user_service, user_repository}
    │     └── context.shared_repositories += {user_repository}
    │
    ├── AuthModule.initialize(context)
    │     └── uses context.shared_repositories["user_repository"]
    │     └── returns {auth_service, token_service, token_repository}
    │
    ├── BookModule.initialize(context)
    │     └── returns {book_service, book_repository}
    │
    ├── HealthModule.initialize(context)
    │     └── returns {health_check_service, health_check_repository}
    │
    └── return AppState(**state, db_engine, **all_services, **all_repos)
            │
            ▼
        app.state = AppState
            │
            ▼
        App Ready to Serve

---