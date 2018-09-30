request = function()
  path = "/resources"
  wrk.headers["Content-Type"] = "application/json"
  wrk.headers["Authorization"] = "Bearer eyJpIjogMCwgInUiOiAiYWRtaW4iLCAidCI6ICIxNTM2OTgxMTc5In0=.a34c19796c0e75ad9ea2df08211d3d7a914f1651d5ce9a3965a60a53cc855092"
  wrk.body = "{\"content\":\"stuff\"}"
  return wrk.format("POST", path)
end

