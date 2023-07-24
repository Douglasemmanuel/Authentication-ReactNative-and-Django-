import { View, Text } from 'react-native'
import React, { useEffect, useState } from 'react'
import { getToken } from '../Services/AsyncStorageService'
import { useGetLoggedUserQuery } from '../Services/UserAuthApi'
import { useDispatch } from 'react-redux'
import { unSetUserInfo } from '../Features/userSlice'
import { setUserInfo } from '../Features/userSlice'
const DashboardScreen = () => {
  const [token, setToken] = useState({})
  const dispatch = useDispatch()
  useEffect(() => {
    (async () => {
      const token = await getToken()
      if (token) {
        const { access, refresh } = JSON.parse(token)
        setToken({
          "access": access,
          "refresh": refresh
        })
        dispatch(setUserAccessToken({ access_token: access }))
      }
    })();
  }, [])
  const { data, isSuccess } = useGetLoggedUserQuery(token.access)
  useEffect(() => {
    if (isSuccess) {
      dispatch(setUserInfo({ email: data.email, name: data.name }))
    }
  })
  return (
    <View>
      <Text>Dashboard Screen</Text>
    </View>
  )
}

export default DashboardScreen